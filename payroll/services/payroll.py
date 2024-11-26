from decimal import Decimal
from typing import Iterator, TypedDict

from django.db import transaction
from django.db.models import F, Q, Sum

from core.models import FinancialYear
from costcentre.models import CostCentre

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


def payroll_forecast_report(cost_centre: CostCentre, financial_year: FinancialYear):
    period_sum_annotations = {
        f"period_{i+1}_sum": Sum(
            F("pay_element__debit_amount") - F("pay_element__credit_amount"),
            filter=Q(**{f"pay_periods__period_{i+1}": True}),
            default=Decimal(0),
        )
        for i in range(12)
    }

    qs = (
        Employee.objects.filter(
            cost_centre=cost_centre,
            pay_periods__year=financial_year,
            pay_element__isnull=False,
        )
        .order_by(
            "programme_code",
            "pay_element__type__group",
        )
        .values(
            "programme_code",
            "pay_element__type__group__natural_code",
            "pay_element__type__group",
            "pay_element__type__group__name",
        )
        .annotate(**period_sum_annotations)
    )

    return qs


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
        .with_basic_pay()
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
