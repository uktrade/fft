from decimal import Decimal
from django.db.models import F, Q, Sum

from costcentre.models import CostCentre
from forecast.models import FinancialCode, ForecastingDataView
from core.models import FinancialYear

from ..models import PayElementTypeGroup, Employee, EmployeePayPeriods


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


def payroll_forecast_report(cost_centre: CostCentre) -> None:
    current_financial_year = FinancialYear.objects.current()

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
            pay_periods__year=current_financial_year,
        )
        .values("pay_element__type__group", "pay_element__type__group__name")
        .annotate(**period_sum_annotations)
    )

    return qs


def cur_payroll_forecast_report(cost_centre: CostCentre) -> None:
    current_financial_year = FinancialYear.objects.current()

    nacs = PayElementTypeGroup.objects.values("natural_code")
    financial_codes = FinancialCode.objects.filter(
        programme__budget_type="DEL",  # FIXME
        cost_centre=cost_centre,
        natural_account_code__in=nacs,
    )

    qs = ForecastingDataView.objects.all()
    qs = qs.filter(financial_code__in=financial_codes)
    qs = qs.filter(financial_year=current_financial_year.financial_year)
    return qs
