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
from payroll.models import Vacancy

from .services import payroll as payroll_service


class EditPayrollView(UserPassesTestMixin, View):
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

    def get_data(self):
        raise NotImplementedError

    def post_data(self, data):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        data = list(self.get_data())
        return JsonResponse({"data": data})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        self.post_data(
            data,
        )
        return JsonResponse({})


# TODO: check user has access to cost centre
class PayrollView(EditPayrollView):
    def get_data(self):
        return payroll_service.get_payroll_data(
            self.cost_centre,
            self.financial_year,
        )

    def post_data(self, data):
        return payroll_service.update_payroll_data(
            self.cost_centre,
            self.financial_year,
            data,
        )


class VacancyView(EditPayrollView):
    def get_data(self):
        return payroll_service.get_vacancies_data(
            self.cost_centre,
            self.financial_year,
        )

    def post_data(self, data):
        return payroll_service.update_vacancies_data(
            self.cost_centre,
            self.financial_year,
            data,
        )


class PayModifierView(EditPayrollView):
    def get_data(self):
        return payroll_service.get_pay_modifiers_data(
            self.cost_centre,
            self.financial_year,
        )

    def post_data(self, data):
        return payroll_service.update_pay_modifiers_data(
            self.cost_centre,
            self.financial_year,
            data,
        )


def redirect_edit_payroll(cost_centre_code, financial_year):
    return redirect(
        "payroll:edit",
        cost_centre_code=cost_centre_code,
        financial_year=financial_year,
    )


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
        "title": "Create Vacancy",
    }
    cost_centre_obj = get_object_or_404(CostCentre, pk=cost_centre_code)

    if request.method == "POST":
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.cost_centre = cost_centre_obj
            vacancy.save()

            payroll_service.vacancy_created(vacancy)

            return redirect_edit_payroll(cost_centre_code, financial_year)
        else:
            context["form"] = form
            return render(request, "payroll/page/vacancy_form.html", context)
    else:
        form = VacancyForm()
        context["form"] = form
    return render(request, "payroll/page/vacancy_form.html", context)


def edit_vacancy_page(
    request: HttpRequest, cost_centre_code: str, financial_year: int, vacancy_id: int
) -> HttpResponse:
    if not request.user.is_superuser:
        raise PermissionDenied

    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

    context = {
        "cost_centre_code": cost_centre_code,
        "financial_year": financial_year,
        "title": "Edit Vacancy",
        "vacancy_id": vacancy.id,
        "is_edit": True,
    }

    if request.method == "POST":
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            vacancy.save()

            return redirect_edit_payroll(cost_centre_code, financial_year)
    else:
        context["form"] = VacancyForm(instance=vacancy)

    return render(request, "payroll/page/vacancy_form.html", context)


def delete_vacancy_page(
    request: HttpRequest, cost_centre_code: str, financial_year: int, vacancy_id: int
) -> HttpResponse:
    if not request.user.is_superuser:
        raise PermissionDenied

    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

    context = {
        "cost_centre_code": cost_centre_code,
        "financial_year": financial_year,
        "vacancy_id": vacancy.id,
    }

    if request.method == "POST":
        vacancy.delete()

        return redirect_edit_payroll(cost_centre_code, financial_year)
    else:
        return render(request, "payroll/page/delete_vacancy.html", context)
