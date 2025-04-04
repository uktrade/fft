import operator
from collections import defaultdict
from itertools import accumulate
from statistics import mean
from typing import Iterator, TypedDict

import numpy as np
import numpy.typing as npt
from django.conf import settings
from django.db import transaction
from django.db.models import Avg, Count, Q

from core.constants import MONTHS, PERIODS
from core.models import Attrition, FinancialYear, PayUplift
from core.types import MonthsDict
from costcentre.models import CostCentre
from forecast.models import FinancialCode, ForecastMonthlyFigure
from forecast.services import FinancialCodeForecastService
from forecast.utils.access_helpers import can_edit_cost_centre, can_edit_forecast
from gifthospitality.models import Grade
from user.models import User

from ..models import Employee, EmployeePayPeriods, Vacancy, VacancyPayPeriods


def employee_created(employee: Employee) -> None:
    """Hook to be called after an employee instance is created."""
    # Create EmployeePayPeriods records for current and future financial years.
    create_pay_periods(employee, pay_period_enabled=employee.is_payroll)
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


def update_all_employee_pay_periods() -> None:
    current_financial_year = FinancialYear.objects.current()

    employee_qs = Employee.objects.exclude(pay_periods__year=current_financial_year)

    pay_periods = (
        EmployeePayPeriods(
            employee=employee,
            year=current_financial_year,
            **{f"period_{i}": employee.is_payroll for i in PERIODS},
        )
        for employee in employee_qs.iterator()
    )

    EmployeePayPeriods.objects.bulk_create(pay_periods)


class PayrollForecast(MonthsDict[int]):
    programme_code: str
    natural_account_code: int


def payroll_forecast_report(
    cost_centre: CostCentre, financial_year: FinancialYear
) -> Iterator[PayrollForecast]:
    # { programme_code: { natural_account_code: np.array[ np.float64 ] } }
    report: dict[str, dict[int, npt.NDArray[np.float64]]] = defaultdict(
        lambda: defaultdict(lambda: np.zeros(12))
    )

    employee_qs = Employee.objects.prefetch_pay_periods(year=financial_year).filter(
        cost_centre=cost_centre,
        pay_periods__year=financial_year,
        has_left=False,
    )
    pay_uplift_obj = PayUplift.objects.filter(financial_year=financial_year).first()
    attrition_obj = get_attrition_instance(financial_year, cost_centre)

    pay_uplift = 1 + np.array(pay_uplift_obj.periods) if pay_uplift_obj else np.ones(12)
    attrition = 1 - np.array(attrition_obj.periods) if attrition_obj else np.ones(12)
    pay_uplift_accumulate = np.array(list(accumulate(pay_uplift, operator.mul)))
    attrition_accumulate = np.array(list(accumulate(attrition, operator.mul)))

    for employee in employee_qs.iterator(chunk_size=2000):
        periods = employee.pay_periods.first().periods
        periods = np.array(periods)

        prog_report = report[employee.programme_code_id]
        prog_report[settings.PAYROLL.BASIC_PAY_NAC] += (
            periods * employee.basic_pay * pay_uplift_accumulate * attrition_accumulate
        )
        prog_report[settings.PAYROLL.PENSION_NAC] += periods * employee.pension
        prog_report[settings.PAYROLL.ERNIC_NAC] += periods * employee.ernic

    vacancy_qs = (
        Vacancy.objects.select_related("grade")
        .prefetch_pay_periods(year=financial_year)
        .filter(
            cost_centre=cost_centre,
            pay_periods__year=financial_year,
        )
    )
    for vacancy in vacancy_qs.iterator(chunk_size=2000):
        avg_salary = get_average_salary_for_grade(vacancy.grade, cost_centre)
        salary = vacancy.fte * avg_salary

        periods = vacancy.pay_periods.first().periods
        periods = np.array(periods)

        prog_report = report[vacancy.programme_code_id]
        prog_report[settings.PAYROLL.VACANCY_NAC] += periods * salary

    for programme_code in report:
        for nac, forecast in report[programme_code].items():
            forecast_floored: list[int] = np.floor(forecast).astype(int).tolist()
            forecast_months: MonthsDict[int] = dict(zip(MONTHS, forecast_floored, strict=False))  # type: ignore

            yield PayrollForecast(
                programme_code=programme_code,
                natural_account_code=nac,
                **forecast_months,
            )


def update_payroll_forecast(
    *, financial_year: FinancialYear, cost_centre: CostCentre
) -> None:
    if cost_centre.is_overseas:
        return

    report = payroll_forecast_report(
        financial_year=financial_year,
        cost_centre=cost_centre,
    )
    for payroll_forecast in report:
        update_payroll_forecast_figure(
            financial_year=financial_year,
            cost_centre=cost_centre,
            payroll_forecast=payroll_forecast,
        )


def update_payroll_forecast_figure(
    *,
    financial_year: FinancialYear,
    cost_centre: CostCentre,
    payroll_forecast: PayrollForecast,
) -> None:
    # Create a financial code if there isn't one.
    financial_code, _ = FinancialCode.objects.get_or_create(
        cost_centre=cost_centre,
        natural_account_code_id=payroll_forecast["natural_account_code"],
        programme_id=payroll_forecast["programme_code"],
        analysis1_code=None,
        analysis2_code=None,
        project_code=None,
    )

    forecast = [payroll_forecast[month] for month in MONTHS]

    FinancialCodeForecastService(
        financial_code=financial_code,
        year=financial_year,
        override_locked=True,
    ).update(forecast)


def get_attrition_instance(
    financial_year: FinancialYear, cost_centre: CostCentre
) -> Attrition | None:
    instance = Attrition.objects.filter(
        financial_year=financial_year, cost_centre=cost_centre
    ).first()

    if instance:
        return instance

    return Attrition.objects.filter(
        financial_year=financial_year, cost_centre=None
    ).first()


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
        employee_qs = (
            Employee.objects.payroll()
            .filter(grade=grade, has_left=False)
            .filter(filter)
        )

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
    notes: str


def get_employee_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> Iterator[EmployeePayroll]:
    qs = (
        Employee.objects.select_related(
            "programme_code__budget_type",
            "grade",
        )
        .prefetch_pay_periods(year=financial_year)
        .filter(
            cost_centre=cost_centre,
            pay_periods__year=financial_year,
            has_left=False,
        )
        .order_by("grade", "id")
    )
    for obj in qs:
        budget_type = obj.programme_code.budget_type
        pay_periods = obj.pay_periods.first()
        yield EmployeePayroll(
            id=obj.pk,
            name=obj.get_full_name(),
            grade=obj.grade.pk,
            employee_no=obj.employee_no,
            fte=obj.fte,
            programme_code=obj.programme_code.pk,
            budget_type=budget_type.budget_type if budget_type else "",
            assignment_status=obj.assignment_status,
            basic_pay=obj.basic_pay,
            pay_periods=pay_periods.periods,
            notes=pay_periods.notes,
        )


@transaction.atomic
def update_employee_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
    data: list[EmployeePayroll],
) -> None:
    """Update a cost centre's employee pay periods for a given year.

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


def update_employee_notes(
    notes: str,
    id: str,
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> None:
    if not id:
        raise ValueError("id is empty")
    period = EmployeePayPeriods.objects.get(
        employee__id=id,
        employee__cost_centre=cost_centre,
        year=financial_year,
    )
    period.notes = notes
    period.save()


def update_vacancy_notes(
    notes: str,
    id: str,
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> None:
    if not id:
        raise ValueError("id is empty")
    period = VacancyPayPeriods.objects.get(
        vacancy__id=id,
        vacancy__cost_centre=cost_centre,
        year=financial_year,
    )
    period.notes = notes
    period.save()


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
    notes: str


def get_vacancies_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> Iterator[Vacancies]:
    qs = (
        Vacancy.objects.select_related(
            "programme_code__budget_type",
            "grade",
        )
        .prefetch_pay_periods(year=financial_year)
        .filter(
            cost_centre=cost_centre,
            pay_periods__year=financial_year,
        )
        .order_by("grade", "id")
    )
    for obj in qs:
        budget_type = obj.programme_code.budget_type
        pay_periods = obj.pay_periods.first()
        yield Vacancies(
            id=obj.pk,
            grade=obj.grade.pk,
            programme_code=obj.programme_code.pk,
            budget_type=budget_type.budget_type if budget_type else "",
            recruitment_type=obj.get_recruitment_type_display(),
            recruitment_stage=obj.get_recruitment_stage_display(),
            appointee_name=obj.appointee_name,
            hiring_manager=obj.hiring_manager,
            hr_ref=obj.hr_ref,
            pay_periods=pay_periods.periods,
            notes=pay_periods.notes,
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
        if not vacancy.get("id"):
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


class PayModifiers(TypedDict):
    global_attrition: list[float]
    attrition: list[float]
    pay_uplift: list[float]


def get_pay_modifiers_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> PayModifiers:
    global_attrition = Attrition.objects.filter(
        financial_year=financial_year, cost_centre=None
    ).first()
    attrition = Attrition.objects.filter(
        financial_year=financial_year, cost_centre=cost_centre
    ).first()
    pay_uplift = PayUplift.objects.filter(
        financial_year=financial_year,
    ).first()

    global_attrition_periods = global_attrition.periods if global_attrition else []
    attrition_periods = attrition.periods if attrition else []
    pay_uplift_periods = pay_uplift.periods if pay_uplift else []

    return {
        "global_attrition": [x * 100 for x in global_attrition_periods],
        "attrition": [x * 100 for x in attrition_periods],
        "pay_uplift": [x * 100 for x in pay_uplift_periods],
    }


def create_default_pay_modifiers(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> None:
    qs = Attrition.objects.filter(
        cost_centre=cost_centre,
        financial_year=financial_year,
    )

    if not qs.exists():
        Attrition.objects.create(cost_centre=cost_centre, financial_year=financial_year)


@transaction.atomic
def update_attrition_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
    data: list[float],
) -> None:
    """Update attrition pay modifier for a given year and cost centre.

    Raises:
        ValueError: If there are not 12 items in the list.
        ValueError: If any of the values are not of type int or float.
    """

    if len(data) != 12:
        raise ValueError("Attrition object should be of length 12")

    if not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Attrition object should be of type int or float")

    attrition = Attrition.objects.get(
        cost_centre=cost_centre,
        financial_year=financial_year,
    )

    attrition.periods = [x / 100 for x in data]
    attrition.clean()
    attrition.save()


def get_actuals_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> dict[str, int]:
    nac_codes = [
        settings.PAYROLL.BASIC_PAY_NAC,
        settings.PAYROLL.PENSION_NAC,
        settings.PAYROLL.ERNIC_NAC,
    ]

    qs = ForecastMonthlyFigure.objects.filter(
        financial_year=financial_year,
        financial_code__cost_centre=cost_centre,
        financial_code__natural_account_code__natural_account_code__in=nac_codes,
        financial_code__project_code__isnull=True,
        archived_status__isnull=True,
    ).select_related(
        "financial_code__cost_centre",
        "financial_code__natural_account_code",
        "financial_code__project_code",
    )

    actuals = {}

    for obj in qs:
        key = obj.financial_code.as_key(
            year=obj.financial_year_id,
            period=obj.financial_period_id,
        )
        actuals[key] = obj.amount

    return actuals


# Permissions
# ===========


def can_access_edit_payroll(user: User) -> bool:
    return user.has_perms(("payroll.view_employee", "payroll.view_vacancy"))


def can_edit_payroll(
    user: User,
    cost_centre: CostCentre,
    financial_year: FinancialYear,
    current_financial_year: int,
) -> bool:
    return (
        can_access_edit_payroll(user)
        and can_edit_forecast(
            user=user,
            financial_year=financial_year.financial_year,
            current_financial_year=current_financial_year,
        )
        and can_edit_cost_centre(
            user=user,
            cost_centre_code=cost_centre.cost_centre_code,
        )
    )
