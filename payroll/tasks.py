from celery import shared_task

from core.models import FinancialYear
from costcentre.models import CostCentre
from payroll.services.payroll import update_payroll_forecast


@shared_task
def update_all_payroll_forecast(*, financial_year: int):
    financial_year_obj = FinancialYear.objects.get(pk=financial_year)

    for cost_centre in CostCentre.objects.all():
        update_payroll_forecast(
            financial_year=financial_year_obj, cost_centre=cost_centre
        )
