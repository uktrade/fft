from decimal import Decimal
from typing import Iterator, TypedDict

from django.db import transaction
from django.db.models import F, Q, Sum

from core.models import FinancialYear
from costcentre.models import CostCentre

from ..models import Employee, EmployeePayPeriods


def employee_created(employee: Employee) -> None:
    """Hook to be called after an employee instance is created."""

    # Create EmployeePayPeriods records for current and future financial years.
    create_employee_pay_periods(employee)

    return None


def create_employee_pay_periods(employee: Employee) -> None:
    current_financial_year = FinancialYear.objects.current()
    future_financial_years = FinancialYear.objects.future()
    financial_years = [current_financial_year] + list(future_financial_years)

    for financial_year in financial_years:
        EmployeePayPeriods.objects.get_or_create(employee=employee, year=financial_year)


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
    name: str
    grade: str
    employee_no: str
    fte: float
    programme_code: str
    budget_type: str
    assignment_status: str
    pay_periods: list[bool]


def get_payroll_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
) -> Iterator[EmployeePayroll]:
    qs = EmployeePayPeriods.objects.select_related(
        "employee__programme_code__budget_type"
    )
    qs = qs.filter(
        employee__cost_centre=cost_centre,
        year=financial_year,
    )
    for obj in qs:
        yield EmployeePayroll(
            name=obj.employee.get_full_name(),
            grade=obj.employee.grade.pk,
            employee_no=obj.employee.employee_no,
            fte=obj.employee.fte,
            programme_code=obj.employee.programme_code.pk,
            budget_type=obj.employee.programme_code.budget_type.budget_type_display,
            assignment_status=obj.employee.assignment_status,
            pay_periods=obj.periods,
        )


@transaction.atomic
def update_payroll_data(
    cost_centre: CostCentre,
    financial_year: FinancialYear,
    payroll_data: list[EmployeePayroll],
) -> None:
    """Update a cost centre payroll for a given year using the provided list.

    This function is wrapped with a transaction, so if any of the payroll updates fail,
    the whole batch will be rolled back.

    Raises:
        ValueError: If an employee_no is empty.
        ValueError: If there are not 12 items in the pay_periods list.
        ValueError: If any of the pay_periods are not of type bool.
    """
    for payroll in payroll_data:
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
