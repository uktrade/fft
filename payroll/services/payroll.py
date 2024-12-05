from collections import defaultdict
from statistics import mean
from typing import Iterator, TypedDict

import numpy as np
import numpy.typing as npt
from django.conf import settings
from django.db import transaction
from django.db.models import Avg, Count, Q

from core.constants import MONTHS
from core.models import FinancialYear
from core.types import MonthsDict
from costcentre.models import CostCentre
from gifthospitality.models import Grade

from ..models import Employee, EmployeePayPeriods, Vacancy, VacancyPayPeriods


def employee_created(employee: Employee) -> None:
    """Hook to be called after an employee instance is created."""
    # Create EmployeePayPeriods records for current and future financial years.
    create_pay_periods(employee)
    return None


def vacancy_created(vacancy: Vacancy) -> None:
    """Hook to be called after a vacancy instance is created."""
    # Create VacancyPayPeriods records for current and future financial years.
    create_pay_periods(vacancy, pay_period_enabled=False)
    return None


def create_pay_periods(instance, pay_period_enabled=None) -> None:
    current_financial_year = FinancialYear.objects.current()
    future_financial_years = FinancialYear.objects.future()
    financial_years = [current_financial_year] + list(future_financial_years)

    pay_periods_model = None
    field_name = ""

    if isinstance(instance, Employee):
        pay_periods_model = EmployeePayPeriods
        field_name = "employee"
    elif isinstance(instance, Vacancy):
        pay_periods_model = VacancyPayPeriods
        field_name = "vacancy"
    else:
        raise ValueError("Unsupported instance type for creating pay periods")

    defaults = {}
    if pay_period_enabled is not None:
        defaults = {f"period_{i+1}": pay_period_enabled for i in range(12)}

    for financial_year in financial_years:
        pay_periods_model.objects.get_or_create(
            defaults=defaults, **{field_name: instance, "year": financial_year}
        )


class PayrollForecast(MonthsDict[float]):
    programme_code: str
    natural_account_code: str


def payroll_forecast_report(
    cost_centre: CostCentre, financial_year: FinancialYear
) -> Iterator[PayrollForecast]:
    # { programme_code: { natural_account_code: np.array[ np.float64 ] } }
    report: dict[str, dict[str, npt.NDArray[np.float64]]] = defaultdict(
        lambda: defaultdict(lambda: np.zeros(12))
    )

    employee_qs = Employee.objects.filter(
        cost_centre=cost_centre,
        pay_periods__year=financial_year,
    )
    for employee in employee_qs.iterator():
        periods = employee.pay_periods.first().periods
        periods = np.array(periods)

        prog_report = report[employee.programme_code_id]
        prog_report[settings.PAYROLL.BASIC_PAY_NAC] += periods * employee.basic_pay
        prog_report[settings.PAYROLL.PENSION_NAC] += periods * employee.pension
        prog_report[settings.PAYROLL.ERNIC_NAC] += periods * employee.ernic

    vacancy_qs = Vacancy.objects.filter(
        cost_centre=cost_centre,
        pay_periods__year=financial_year,
    )
    for vacancy in vacancy_qs.iterator():
        avg_salary = get_average_salary_for_grade(vacancy.grade, cost_centre)
        salary = vacancy.fte * avg_salary

        periods = vacancy.pay_periods.first().periods
        periods = np.array(periods)

        prog_report = report[vacancy.programme_code_id]
        prog_report[settings.PAYROLL.VACANCY_NAC] += periods * salary

    for programme_code in report:
        for nac, forecast in report[programme_code].items():
            forecast_months: MonthsDict[float] = dict(zip(MONTHS, forecast, strict=False))  # type: ignore

            yield PayrollForecast(
                programme_code=programme_code,
                natural_account_code=nac,
                **forecast_months,
            )


# TODO (FFT-131): Apply caching to the average salary calculation
def get_average_salary_for_grade(grade: Grade, cost_centre: CostCentre) -> int:
    employee_count_threshold = settings.PAYROLL.AVERAGE_SALARY_THRESHOLD

    # Expanding scope filters which start at the cost centre and end at all employees.
    filters = [
        Q(cost_centre=cost_centre),
        Q(cost_centre__directorate=cost_centre.directorate),
        Q(cost_centre__directorate__group=cost_centre.directorate.group),
        Q(),
    ]

    salaries: list[int] = []

    for filter in filters:
        employee_qs = Employee.objects.payroll().filter(grade=grade).filter(filter)

        basic_pay = employee_qs.aggregate(
            count=Count("basic_pay"), avg=Avg("basic_pay")
        )

        if basic_pay["count"] >= employee_count_threshold:
            return basic_pay["avg"]

        if basic_pay["count"]:
            salaries += list(employee_qs.values_list("basic_pay", flat=True))

    if salaries:
        return round(mean(salaries))  # pence

    # TODO: What do we do if there were no employees at all found at that grade?
    return 0


class EmployeePayroll(TypedDict):
    id: int
    name: str
    grade: str
    employee_no: str
    fte: float
    programme_code: str
    budget_type: str
    assignment_status: str
    basic_pay: float
    pay_periods: list[bool]


def get_payroll_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> Iterator[EmployeePayroll]:
    qs = (
        Employee.objects.select_related(
            "programme_code__budget_type",
        )
        .prefetch_related(
            "pay_periods",
        )
        .filter(
            cost_centre=cost_centre,
            pay_periods__year=financial_year,
        )
    )
    for obj in qs:
        yield EmployeePayroll(
            id=obj.pk,
            name=obj.get_full_name(),
            grade=obj.grade.pk,
            employee_no=obj.employee_no,
            fte=obj.fte,
            programme_code=obj.programme_code.pk,
            budget_type=obj.programme_code.budget_type.budget_type_display,
            assignment_status=obj.assignment_status,
            basic_pay=obj.basic_pay,
            # `first` is OK as there should only be one `pay_periods` with the filters.
            pay_periods=obj.pay_periods.first().periods,
        )


@transaction.atomic
def update_payroll_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
    data: list[EmployeePayroll],
) -> None:
    """Update a cost centre payroll for a given year using the provided list.

    This function is wrapped with a transaction, so if any of the payroll updates fail,
    the whole batch will be rolled back.

    Raises:
        ValueError: If an employee_no is empty.
        ValueError: If there are not 12 items in the pay_periods list.
        ValueError: If any of the pay_periods are not of type bool.
    """
    for payroll in data:
        if not payroll["employee_no"]:
            raise ValueError("employee_no is empty")

        if len(payroll["pay_periods"]) != 12:
            raise ValueError("pay_periods list should be of length 12")

        if not all(isinstance(x, bool) for x in payroll["pay_periods"]):
            raise ValueError("pay_periods items should be of type bool")

        pay_periods = EmployeePayPeriods.objects.get(
            employee__employee_no=payroll["employee_no"],
            employee__cost_centre=cost_centre,
            year=financial_year,
        )
        pay_periods.periods = payroll["pay_periods"]
        pay_periods.save()


class Vacancies(TypedDict):
    id: int
    grade: str
    programme_code: str
    budget_type: str
    recruitment_type: str
    recruitment_stage: str
    appointee_name: str
    hiring_manager: str
    hr_ref: str
    pay_periods: list[bool]


def get_vacancies_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> Iterator[Vacancies]:
    qs = (
        Vacancy.objects.filter(
            cost_centre=cost_centre,
            pay_periods__year=financial_year,
        )
        .prefetch_related(
            "pay_periods",
        )
        .filter(
            cost_centre=cost_centre,
            pay_periods__year=financial_year,
        )
    )
    for obj in qs:
        yield Vacancies(
            id=obj.pk,
            grade=obj.grade.pk,
            programme_code=obj.programme_code.pk,
            budget_type=obj.programme_code.budget_type.budget_type_display,
            recruitment_type=obj.get_recruitment_type_display(),
            recruitment_stage=obj.get_recruitment_stage_display(),
            appointee_name=obj.appointee_name,
            hiring_manager=obj.hiring_manager,
            hr_ref=obj.hr_ref,
            # `first` is OK as there should only be one `pay_periods` with the filters.
            pay_periods=obj.pay_periods.first().periods,
        )


@transaction.atomic
def update_vacancies_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
    data: list[Vacancies],
) -> None:
    """Update a cost centre vacancies for a given year using the provided list.

    This function is wrapped with a transaction, so if any of the vacancy updates fail,
    the whole batch will be rolled back.

    Raises:
        ValueError: If a vacancy id is empty.
        ValueError: If there are not 12 items in the pay_periods list.
        ValueError: If any of the pay_periods are not of type bool.
    """

    for vacancy in data:
        if not vacancy["id"]:
            raise ValueError("id is empty")

        if len(vacancy["pay_periods"]) != 12:
            raise ValueError("pay_periods list should be of length 12")

        if not all(isinstance(x, bool) for x in vacancy["pay_periods"]):
            raise ValueError("pay_periods items should be of type bool")

        pay_periods = VacancyPayPeriods.objects.get(
            vacancy__id=vacancy["id"],
            vacancy__cost_centre=cost_centre,
            year=financial_year,
        )
        pay_periods.periods = vacancy["pay_periods"]
        pay_periods.save()
