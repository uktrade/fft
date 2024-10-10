from dataclasses import asdict, dataclass
from functools import wraps
import json
from django.http import HttpResponse, HttpRequest, JsonResponse
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


@dataclass
class EmployeePayroll:
    name: str
    employee_no: str
    period_1: bool
    period_2: bool
    period_3: bool
    period_4: bool
    period_5: bool
    period_6: bool
    period_7: bool
    period_8: bool
    period_9: bool
    period_10: bool
    period_11: bool
    period_12: bool


@dataclass
class EmployeePayrollPayload:
    payload: list[EmployeePayroll]


@superuser_view
def edit_payroll_page(
    request: HttpRequest, cost_centre_code: str, financial_year: int
) -> HttpResponse:
    cost_centre = get_object_or_404(CostCentre, pk=cost_centre_code)
    financial_year = get_object_or_404(FinancialYear, pk=financial_year)

    if request.method == "GET":
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
                "period_1",
                "period_2",
                "period_3",
                "period_4",
                "period_5",
                "period_6",
                "period_7",
                "period_8",
                "period_9",
                "period_10",
                "period_11",
                "period_12",
                employee_no=F("employee__employee_no"),
            )
        )
        payroll_data = list(payroll_qs)

        context = {
            "payroll_data": payroll_data,
        }
        return TemplateResponse(request, "payroll/page/edit_payroll.html", context)
    elif request.method == "POST":
        errors = []

        payload = json.loads(request.body)["payload"]

        try:
            employee_payroll = [EmployeePayroll(**x) for x in payload]
        except TypeError as err:
            errors.append(str(err))
            return JsonResponse({"errors": errors, "data": None})

        for record in employee_payroll:
            employee_pay_periods = EmployeePayPeriods.objects.get(
                employee__employee_no=record.employee_no,
                year=financial_year,
            )
            employee_pay_periods.period_1 = record.period_1
            employee_pay_periods.period_2 = record.period_2
            employee_pay_periods.period_3 = record.period_3
            employee_pay_periods.period_4 = record.period_4
            employee_pay_periods.period_5 = record.period_5
            employee_pay_periods.period_6 = record.period_6
            employee_pay_periods.period_7 = record.period_7
            employee_pay_periods.period_8 = record.period_8
            employee_pay_periods.period_9 = record.period_9
            employee_pay_periods.period_10 = record.period_10
            employee_pay_periods.period_11 = record.period_11
            employee_pay_periods.period_12 = record.period_12
            employee_pay_periods.save()

        data = [asdict(x) for x in employee_payroll]

        assert not errors

        return JsonResponse({"errors": errors, "data": data})


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
