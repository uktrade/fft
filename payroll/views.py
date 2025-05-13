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
from payroll.models import Employee, Vacancy

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

    def form_valid(self, form):
        response = super().form_valid(form)

        payroll_service.vacancy_updated(self.object)

        return response


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

    def form_valid(self, form):
        response = super().form_valid(form)

        payroll_service.vacancy_deleted(self.object)

        return response


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


def build_row(model, extra_fields=None):
    pay_periods = model.pay_periods.first()
    row = {
        "grade": model.grade,
        "fte": model.fte,
        "cost_centre_id": model.cost_centre_id,
        "cost_centre_name": model.cost_centre.cost_centre_name,
        "directorate": model.cost_centre.directorate.directorate_name,
        "group_name": model.cost_centre.directorate.group.group_name,
        "programme_code": model.programme_code.programme_code,
        "april": pay_periods.period_1,
        "may": pay_periods.period_2,
        "june": pay_periods.period_3,
        "july": pay_periods.period_4,
        "august": pay_periods.period_5,
        "september": pay_periods.period_6,
        "october": pay_periods.period_7,
        "november": pay_periods.period_8,
        "december": pay_periods.period_9,
        "january": pay_periods.period_10,
        "february": pay_periods.period_11,
        "march": pay_periods.period_12,
        "narrative": pay_periods.notes,
        "budget_type": model.programme_code.budget_type.budget_type,  # Not the quite right format
    }
    if extra_fields:
        row.update(extra_fields)
    return row


def payroll_data_report(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        raise PermissionDenied

    context = {}
    rows = []

    # Filter to financial year
    employees = Employee.objects.all()
    vacancies = Vacancy.objects.all()

    for employee in employees:
        rows.append(
            build_row(
                employee,
                extra_fields={
                    "first_name": employee.first_name,
                    "last_name": employee.last_name,
                    "employee_no": employee.employee_no,
                    "wmi_payroll": (
                        "Payroll" if employee.basic_pay > 0 else "Non-payroll"
                    ),
                    "assignment_status": employee.assignment_status,
                    "person_type": "Employee",
                    "salary": f"{employee.basic_pay / 100:.2f}",
                    "recruitment_type": "N/A",
                    "HR_stage": "N/A",
                    "HR_ref": "N/A",
                    "vacancy_type": "N/A",
                    "programme_switch": "N/A",
                    # "capital":
                    # "recharge":
                    # "reason":
                    "fte_total": employee.fte * 12,
                },
            ),
        )

    for vacancy in vacancies:
        rows.append(
            build_row(
                employee,
                extra_fields={
                    "first_name": "Vacancy",
                    "last_name": "Vacancy",
                    "employee_no": "1",  # This is what vacancies are set to in the test data
                    "wmi_payroll": "Vacancy",
                    "assignment_status": "N/A",
                    "person_type": "Vacancy",
                    # "salary":
                    "recruitment_type": vacancy.get_recruitment_type_display(),
                    "HR_stage": vacancy.get_recruitment_stage_display(),
                    "HR_ref": vacancy.hr_ref,
                    # "vacancy_type":
                    # "programme_switch":
                    # "capital":
                    # "recharge":
                    # "reason":
                    "fte_total": "0",  # This is what vacancies are set to in the test data
                },
            )
        )

    context = {"rows": rows}

    return TemplateResponse(request, "payroll/page/payroll_data_report.html", context)
