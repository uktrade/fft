import waffle
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.base import ContextMixin, TemplateView

from config import flags
from core.models import FinancialYear
from costcentre.models import CostCentre
from payroll.forms import VacancyForm
from payroll.models import Vacancy

from .services import payroll as payroll_service
from .services.ingest import import_payroll


class EditPayrollBaseView(UserPassesTestMixin, ContextMixin, View):
    def test_func(self) -> bool | None:
        if not waffle.flag_is_active(self.request, flags.EDIT_PAYROLL):
            return False

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

    def get_context_data(self, **kwargs):
        context = {
            "cost_centre": self.cost_centre,
            "financial_year": self.financial_year,
        }
        return super().get_context_data(**kwargs) | context


class EditPayrollPage(TemplateView, EditPayrollBaseView):
    template_name = "payroll/page/edit_payroll.html"


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
            "title": "Add vacancy",
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
            "title": "Edit vacancy",
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
        if "payroll_csv" not in request.FILES:
            context = {"error": "Payroll file is required"}
        else:
            payroll_csv = request.FILES["payroll_csv"]
            output = import_payroll(payroll_csv)

    context = {
        "output": output,
    }

    return TemplateResponse(request, "payroll/page/import_payroll.html", context)
