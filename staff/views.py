from functools import wraps
from django.http import HttpResponse, HttpRequest
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from core.models import FinancialYear
from costcentre.models import CostCentre
from staff.services.staff import payroll_forecast_report, cur_payroll_forecast_report

from .models import StaffForecast


# TODO: Remove once no longer needed.
def superuser_view(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(*args, **kwargs)

    return wrapper


@superuser_view
def edit_payroll_page(request: HttpRequest) -> HttpResponse:
    context = {}
    return TemplateResponse(request, "staff/page/edit_payroll.html", context)


@superuser_view
def staff_debug_page(request: HttpRequest) -> HttpResponse:
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

    staff_forecast = StaffForecast.objects.filter(
        staff__cost_centre=cost_centre,
        year=financial_year,
    )

    context = {
        "cost_centre": cost_centre,
        "financial_year": financial_year,
        "staff_forecast": staff_forecast,
        "new_payroll_forecast_report": payroll_forecast_report(cost_centre),
        "cur_payroll_forecast_report": cur_payroll_forecast_report(cost_centre),
    }

    return TemplateResponse(request, "staff/page/debug.html", context)
