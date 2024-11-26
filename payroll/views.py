import json

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.views import View

from core.models import FinancialYear
from costcentre.models import CostCentre
from payroll.forms import VacancyForm

from .services import payroll as payroll_service


class PositionView(UserPassesTestMixin, View):
    def test_func(self) -> bool | None:
        return self.request.user.is_superuser

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
        get_function_name = self.get_service_get_name()
        get_function = getattr(payroll_service, get_function_name)

        data = list(
            get_function(
                cost_centre=self.cost_centre,
                financial_year=self.financial_year,
            )
        )
        return JsonResponse({"data": data})

    def post(self, request, *args, **kwargs):
        post_function_name = self.get_service_post_name()
        post_function = getattr(payroll_service, post_function_name)

        data = json.loads(request.body)

        post_function(
            cost_centre=self.cost_centre,
            financial_year=self.financial_year,
            data=data,
        )
        return JsonResponse({})


# TODO: check user has access to cost centre
class PayrollView(PositionView):
    def get_service_get_name(self):
        return "get_payroll_data"

    def get_service_post_name(self):
        return "update_payroll_data"


class VacancyView(PositionView):
    def get_service_get_name(self):
        return "get_vacancies_data"

    def get_service_post_name(self):
        return "update_vacancies_data"


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
    cost_centre_code = cost_centre_obj.cost_centre_code
    financial_year = financial_year_obj.financial_year

    context = {
        "cost_centre_code": cost_centre_code,
        "financial_year": financial_year,
        "payroll_forecast_report": payroll_forecast_report_data,
        "months": [
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
            "Jan",
            "Feb",
            "Mar",
        ],
    }

    return TemplateResponse(request, "payroll/page/edit_payroll.html", context)


def add_vacancy_page(
    request: HttpRequest, cost_centre_code: str, financial_year: int
) -> HttpResponse:
    if not request.user.is_superuser:
        raise PermissionDenied

    context = {
        "cost_centre_code": cost_centre_code,
        "financial_year": financial_year,
    }
    cost_centre_obj = get_object_or_404(CostCentre, pk=cost_centre_code)

    if request.method == "POST":
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.cost_centre = cost_centre_obj
            vacancy.save()

            payroll_service.vacancy_created(vacancy)

            return redirect(
                "payroll:edit",
                cost_centre_code=cost_centre_code,
                financial_year=financial_year,
            )
        else:
            context["form"] = form
            return render(request, "payroll/page/add_vacancy.html", context)
    else:
        form = VacancyForm()
        context["form"] = form
    return render(request, "payroll/page/add_vacancy.html", context)
