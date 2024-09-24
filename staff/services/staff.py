from decimal import Decimal
from django.db.models import F, Q, Sum

from costcentre.models import CostCentre
from staff.models import PayElementGroup, Staff, StaffForecast
from forecast.models import FinancialCode, ForecastingDataView
from core.models import FinancialYear


def staff_created(staff: Staff) -> None:
    """Hook to be called after a staff instance is created."""

    # Create StaffForecast records for current and future financial years.
    create_staff_forecast(staff)

    return None


def create_staff_forecast(staff: Staff) -> None:
    current_financial_year = FinancialYear.objects.current()
    future_financial_years = FinancialYear.objects.future()
    financial_years = [current_financial_year] + list(future_financial_years)

    for financial_year in financial_years:
        StaffForecast.objects.get_or_create(staff=staff, year=financial_year)


def payroll_forecast_report(cost_centre: CostCentre) -> None:
    current_financial_year = FinancialYear.objects.current()

    period_sum_annotations = {
        f"period_{i+1}_sum": Sum(
            F("payroll__debit_amount") - F("payroll__credit_amount"),
            filter=Q(**{f"forecast__period_{i+1}": True}),
            default=Decimal(0),
        )
        for i in range(12)
    }

    qs = (
        Staff.objects.filter(
            cost_centre=cost_centre,
            forecast__year=current_financial_year,
        )
        .values("payroll__pay_element__group", "payroll__pay_element__group__name")
        .annotate(**period_sum_annotations)
    )

    return qs


def cur_payroll_forecast_report(cost_centre: CostCentre) -> None:
    current_financial_year = FinancialYear.objects.current()

    nacs = PayElementGroup.objects.values("natural_code")
    financial_codes = FinancialCode.objects.filter(
        programme__budget_type="DEL",  # FIXME
        cost_centre=cost_centre,
        natural_account_code__in=nacs,
    )

    qs = ForecastingDataView.objects.all()
    qs = qs.filter(financial_code__in=financial_codes)
    qs = qs.filter(financial_year=current_financial_year.financial_year)
    return qs
