import json

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views import View

from core.models import FinancialYear
from costcentre.models import CostCentre

from .services import payroll as payroll_service


# TODO: check user has access to cost centre
class PayrollView(View):
    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.cost_centre = get_object_or_404(
            CostCentre,
            pk=self.kwargs["cost_centre_code"],
        )
        self.financial_year = get_object_or_404(
            FinancialYear,
            pk=self.kwargs["financial_year"],
        )

    def get(self, request, *args, **kwargs):
        data = list(
            payroll_service.get_payroll_data(
                cost_centre=self.cost_centre,
                financial_year=self.financial_year,
            )
        )
        return JsonResponse({"data": data})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        payroll_service.update_payroll_data(
            cost_centre=self.cost_centre,
            financial_year=self.financial_year,
            payroll_data=data,
        )
        return JsonResponse({})


def edit_payroll_page(
    request: HttpRequest, cost_centre_code: str, financial_year: int
) -> HttpResponse:
    if not request.user.is_superuser:
        raise PermissionDenied

    cost_centre_obj = get_object_or_404(CostCentre, pk=cost_centre_code)
    financial_year_obj = get_object_or_404(FinancialYear, pk=financial_year)
    payroll_forecast_report_data = payroll_service.payroll_forecast_report(
        cost_centre_obj, financial_year_obj
    )

    context = {
        "cost_centre_code": cost_centre_obj.cost_centre_code,
        "financial_year": financial_year_obj.financial_year,
        "payroll_forecast_report": payroll_forecast_report_data,
        "months": ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'],

    }

    return TemplateResponse(request, "payroll/page/edit_payroll.html", context)
