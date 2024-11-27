from decimal import Decimal
from typing import Iterator, TypedDict

from django.db import transaction
from django.db.models import F, Q, Sum, Avg, Count

from core.models import FinancialYear
from costcentre.models import CostCentre
from gifthospitality.models import Grade

from ..models import (
    Employee,
    EmployeePayPeriods,
    Vacancy,
    VacancyPayPeriods,
)


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


def payroll_forecast_report(cost_centre: CostCentre, financial_year: FinancialYear):
    from collections import defaultdict

    # programme_code: nac: {data}
    report: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    months = [
        "period_1_sum",
        "period_2_sum",
        "period_3_sum",
        "period_4_sum",
        "period_5_sum",
        "period_6_sum",
        "period_7_sum",
        "period_8_sum",
        "period_9_sum",
        "period_10_sum",
        "period_11_sum",
        "period_12_sum",
    ]
    pay_type_to_nac = {
        "basic_pay": "71111001",
        "ernic": "71111002",
        "pension": "71111003",
    }

    employee_qs = Employee.objects.filter(
        cost_centre=cost_centre,
        pay_periods__year=financial_year,
    )
    for employee in employee_qs.iterator():
        periods = employee.pay_periods.first().periods
        for i, month in enumerate(months):
            if not periods[i]:
                continue

            report[employee.programme_code_id]["basic_pay"][month] += employee.basic_pay
            report[employee.programme_code_id]["pension"][month] += employee.pension
            report[employee.programme_code_id]["ernic"][month] += employee.ernic

    vacancy_qs = Vacancy.objects.filter(
        cost_centre=cost_centre,
        pay_periods__year=financial_year,
    )
    for vacancy in vacancy_qs.iterator():
        salary = get_salary_for_vacancy(vacancy)

        periods = vacancy.pay_periods.first().periods
        for i, month in enumerate(months):
            if not periods[i]:
                continue

            report[vacancy.programme_code_id]["basic_pay"][month] += salary

    for programme_code in report:
        for pay_type in report[programme_code]:
            yield {
                "programme_code": programme_code,
                "pay_element__type__group__natural_code": pay_type_to_nac[pay_type],
                "pay_element__type__group__name": pay_type,
                **report[programme_code][pay_type],
            }


def get_salary_for_vacancy(vacancy: Vacancy) -> int:
    return get_average_salary_for_grade(vacancy.grade, vacancy.cost_centre)


def get_average_salary_for_grade(grade: Grade, cost_centre: CostCentre | None) -> int:
    from statistics import mean

    filters = []

    if cost_centre:
        filters += [
            Q(cost_centre=cost_centre),
            Q(cost_centre__directorate=cost_centre.directorate),
            Q(cost_centre__directorate__group=cost_centre.directorate.group),
        ]

    filters += [Q()]

    salaries = []

    for filter in filters:
        employee_qs = Employee.objects.filter(grade=grade, basic_pay__gt=0).filter(
            filter
        )

        basic_pay_stats = employee_qs.aggregate(Count("basic_pay"), Avg("basic_pay"))
        salaries.append(basic_pay_stats["basic_pay__avg"])

        if basic_pay_stats["basic_pay__count"] >= 2:
            return basic_pay_stats["basic_pay__avg"]

    return mean(salaries)


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
        # .with_basic_pay()
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
