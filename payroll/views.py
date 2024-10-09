from functools import wraps
from django.http import HttpResponse, HttpRequest
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import F, Value
from django.db.models.functions import Concat

from core.models import FinancialYear
from costcentre.models import CostCentre
from payroll.services.payroll import (
    payroll_forecast_report,
    cur_payroll_forecast_report,
)

from .models import EmployeePayPeriods


# TODO: Remove once no longer needed.
def superuser_view(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper


@superuser_view
def edit_payroll_page(
    request: HttpRequest, cost_centre_code: str, financial_year: int
) -> HttpResponse:
    cost_centre = get_object_or_404(CostCentre, pk=cost_centre_code)
    financial_year = get_object_or_404(FinancialYear, pk=financial_year)

    payroll_qs = (
        EmployeePayPeriods.objects.filter(
            employee__cost_centre=cost_centre,
            year=financial_year,
        )
        .annotate(
            name=Concat("employee__first_name", Value(" "), "employee__last_name"),
        )
        .values(
            "name",
            employee_no=F("employee__employee_no"),
            apr=F("period_1"),
            may=F("period_2"),
            jun=F("period_3"),
            jul=F("period_4"),
            aug=F("period_5"),
            sep=F("period_6"),
            oct=F("period_7"),
            nov=F("period_8"),
            dec=F("period_9"),
            jan=F("period_10"),
            feb=F("period_11"),
            mar=F("period_12"),
        )
    )
    payroll_data = list(payroll_qs)

    context = {
        "payroll_data": payroll_data,
    }
    return TemplateResponse(request, "payroll/page/edit_payroll.html", context)


@superuser_view
def payroll_debug_page(request: HttpRequest) -> HttpResponse:
    if request.GET.get("cost_centre"):
        cost_centre = CostCentre.objects.get(pk=request.GET.get("cost_centre"))
    else:
        cost_centre = CostCentre.objects.first()

    if request.GET.get("financial_year"):
        financial_year = FinancialYear.objects.get(
            financial_year=request.GET.get("financial_year")
        )
    else:
        financial_year = FinancialYear.objects.current()

    employee_pay_periods = EmployeePayPeriods.objects.filter(
        employee__cost_centre=cost_centre,
        year=financial_year,
    )

    context = {
        "cost_centre": cost_centre,
        "financial_year": financial_year,
        "employee_pay_periods": employee_pay_periods,
        "new_payroll_forecast_report": payroll_forecast_report(cost_centre),
        "cur_payroll_forecast_report": cur_payroll_forecast_report(cost_centre),
    }

    return TemplateResponse(request, "payroll/page/debug.html", context)
