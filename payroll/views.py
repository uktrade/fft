import json

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from core.constants import MONTHS
from core.models import FinancialYear
from costcentre.models import CostCentre
from payroll.forms import VacancyForm
from payroll.models import Vacancy

from .services import payroll as payroll_service
from .services.ingest import import_payroll


class EditPayrollBaseView(UserPassesTestMixin, View):
    def test_func(self) -> bool | None:
        return payroll_service.can_edit_payroll(
            self.request.user,
            self.cost_centre,
            self.financial_year,
            self.request.current_financial_year,
        )

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


class EditPayrollApiView(EditPayrollBaseView):
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


class EmployeeApiView(EditPayrollApiView):
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


class VacancyApiView(EditPayrollApiView):
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


class PayModifierApiView(EditPayrollApiView):
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


class EditPayrollPage(EditPayrollBaseView):
    def get(self, *args, **kwargs) -> HttpResponse:
        payroll_forecast_report_data = payroll_service.payroll_forecast_report(
            self.cost_centre, self.financial_year
        )

        context = {
            "cost_centre_code": self.cost_centre.cost_centre_code,
            "financial_year": self.financial_year.financial_year,
            "payroll_forecast_report": payroll_forecast_report_data,
            "months": MONTHS,
        }

        return TemplateResponse(self.request, "payroll/page/edit_payroll.html", context)


class VacancyViewMixin(PermissionRequiredMixin):
    model = Vacancy
    pk_url_kwarg = "vacancy_id"

    def get_success_url(self):
        return reverse(
            "payroll:edit",
            kwargs={
                "cost_centre_code": self.cost_centre.cost_centre_code,
                "financial_year": self.financial_year.financial_year,
            },
        )


class AddVacancyView(VacancyViewMixin, CreateView, EditPayrollBaseView):
    form_class = VacancyForm
    permission_required = "payroll.add_vacancy"
    template_name = "payroll/page/vacancy_form.html"

    def get_context_data(self, **kwargs):
        context = {
            "cost_centre_code": self.cost_centre.cost_centre_code,
            "financial_year": self.financial_year.financial_year,
            "title": "Create Vacancy",
        }
        return super().get_context_data(**kwargs) | context

    def form_valid(self, form):
        form.instance.cost_centre = self.cost_centre

        response = super().form_valid(form)

        payroll_service.vacancy_created(self.object)

        return response


class EditVacancyView(VacancyViewMixin, UpdateView, EditPayrollBaseView):
    form_class = VacancyForm
    template_name = "payroll/page/vacancy_form.html"
    permission_required = "payroll.change_vacancy"

    def get_context_data(self, **kwargs):
        context = {
            "cost_centre_code": self.cost_centre.cost_centre_code,
            "financial_year": self.financial_year.financial_year,
            "title": "Edit Vacancy",
            "vacancy_id": self.object.id,
            "is_edit": True,
        }
        return super().get_context_data(**kwargs) | context


class DeleteVacancyView(VacancyViewMixin, DeleteView, EditPayrollBaseView):
    template_name = "payroll/page/delete_vacancy.html"
    permission_required = "payroll.delete_vacancy"

    def get_context_data(self, **kwargs):
        context = {
            "cost_centre_code": self.cost_centre.cost_centre_code,
            "financial_year": self.financial_year.financial_year,
            "vacancy_id": self.object.id,
        }
        return super().get_context_data(**kwargs) | context


def import_payroll_page(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        raise PermissionDenied

    output = ""
    context = {}
    if request.method == "POST":
        if "hr_csv" not in request.FILES or "payroll_csv" not in request.FILES:
            context = {"error": "Both HR and Payroll files are required"}
        else:
            hr_csv = request.FILES["hr_csv"]
            hr_csv_has_header = request.POST.get("hr_csv_has_header", False)
            payroll_csv = request.FILES['payroll_csv']
            payroll_csv_has_header = request.POST.get("hr_csv_has_header", False)
            output = import_payroll(
                hr_csv,
                payroll_csv,
                hr_csv_has_header,
                payroll_csv_has_header
            )

            context = {
                "output": output,
            }
    return TemplateResponse(request, "payroll/page/import_payroll.html", context)
