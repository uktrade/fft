import csv
import datetime as dt

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.base import ContextMixin, TemplateView

import payroll.services.vacancy
from core.models import FinancialYear
from costcentre.models import CostCentre
from forecast.utils.access_helpers import get_user_cost_centres
from payroll.constants import PAYROLL_REPORT_FIELDS
from payroll.forms import VacancyForm
from payroll.models import Employee, Position, Vacancy
from user.models import User

from .services import payroll as payroll_service
from .services.ingest import import_payroll


class EditPayrollBaseView(UserPassesTestMixin, ContextMixin, View):
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

        payroll.services.vacancy.vacancy_created(self.object)

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

        payroll.services.vacancy.vacancy_updated(self.object)

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

        payroll.services.vacancy.vacancy_deleted(self.object)

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
            payroll_period = int(request.POST["payroll_period"])
            output = import_payroll(payroll_csv, payroll_period)

    context = {
        "output": output,
    }

    return TemplateResponse(request, "payroll/page/import_payroll.html", context)


def build_row(model: Position, extra_fields: dict[str, str]):
    pay_periods = model.pay_periods.first()
    budget_type = (
        model.programme_code.budget_type.budget_type
        if model.programme_code.budget_type
        else ""
    )
    row = {
        "grade": model.grade,
        "fte": model.fte,
        "cost_centre_id": model.cost_centre_id,
        "cost_centre_name": model.cost_centre.cost_centre_name,
        "directorate": model.cost_centre.directorate.directorate_name,
        "group_name": model.cost_centre.directorate.group.group_name,
        "programme_code": model.programme_code.programme_code,
        "april": int(pay_periods.period_1),
        "may": int(pay_periods.period_2),
        "june": int(pay_periods.period_3),
        "july": int(pay_periods.period_4),
        "august": int(pay_periods.period_5),
        "september": int(pay_periods.period_6),
        "october": int(pay_periods.period_7),
        "november": int(pay_periods.period_8),
        "december": int(pay_periods.period_9),
        "january": int(pay_periods.period_10),
        "february": int(pay_periods.period_11),
        "march": int(pay_periods.period_12),
        "fte_april": int(pay_periods.period_1) * model.fte,
        "fte_may": int(pay_periods.period_2) * model.fte,
        "fte_june": int(pay_periods.period_3) * model.fte,
        "fte_july": int(pay_periods.period_4) * model.fte,
        "fte_august": int(pay_periods.period_5) * model.fte,
        "fte_september": int(pay_periods.period_6) * model.fte,
        "fte_october": int(pay_periods.period_7) * model.fte,
        "fte_november": int(pay_periods.period_8) * model.fte,
        "fte_december": int(pay_periods.period_9) * model.fte,
        "fte_january": int(pay_periods.period_10) * model.fte,
        "fte_february": int(pay_periods.period_11) * model.fte,
        "fte_march": int(pay_periods.period_12) * model.fte,
        "capital": budget_type,
        "recharge": "",
        "reason": "",
        "narrative": pay_periods.notes,
        "fte_total": f"{sum(pay_periods.periods) * model.fte}",
        "budget_type": budget_type,
        "cc_name_number": f"{model.cost_centre_id} - {model.cost_centre.cost_centre_name}",
    }
    if extra_fields:
        row.update(extra_fields)
    return row


def get_report_data(user: User, financial_year: FinancialYear) -> list[dict[str, str]]:
    user_cost_centres = get_user_cost_centres(user)
    rows: list[dict[str, str]] = []

    employees = (
        Employee.objects.filter(has_left=False, cost_centre__in=user_cost_centres)
        .prefetch_pay_periods(year=financial_year)
        .select_related(
            "cost_centre__directorate__group", "grade", "programme_code__budget_type"
        )
        .with_total_cost()
    )
    vacancies = (
        Vacancy.objects.filter(cost_centre__in=user_cost_centres)
        .prefetch_pay_periods(year=financial_year)
        .select_related(
            "cost_centre__directorate__group", "grade", "programme_code__budget_type"
        )
    )

    for employee in employees:
        rows.append(
            build_row(
                employee,
                extra_fields={
                    "first_name": employee.first_name,
                    "last_name": employee.last_name,
                    "employee_no": employee.employee_no,
                    "wmi_payroll": (
                        "Payroll" if employee.is_payroll else "Non-payroll"
                    ),
                    "assignment_status": employee.assignment_status,
                    "person_type": "Employee",
                    "payroll_cost_centre": employee.cost_centre_id,
                    "salary": f"{employee.total_cost / 100:.2f}",
                    "recruitment_type": "N/A",
                    "HR_stage": "N/A",
                    "HR_ref": "N/A",
                    "vacancy_type": "N/A",
                    "programme_switch": "N/A",
                    "employee_name": f"{employee.first_name} {employee.last_name}",
                    "employee_prog_code": f"{employee.first_name} {employee.last_name} ({employee.programme_code})",
                },
            ),
        )

    for vacancy in vacancies:
        rows.append(
            build_row(
                vacancy,
                extra_fields={
                    "first_name": "Vacancy",
                    "last_name": "Vacancy",
                    "employee_no": "1",
                    "wmi_payroll": "Vacancy",
                    "assignment_status": "N/A",
                    "person_type": "Vacancy",
                    "payroll_cost_centre": "N/A",
                    "salary": f"{payroll_service.get_average_cost_for_grade(
                        vacancy.grade, vacancy.cost_centre
                    ).total_cost / 100:.2f}",
                    "recruitment_type": vacancy.get_recruitment_type_display(),
                    "HR_stage": vacancy.get_recruitment_stage_display(),
                    "HR_ref": vacancy.hr_ref,
                    "vacancy_type": "",
                    "programme_switch": "",
                    "employee_name": "Vacancy Vacancy",
                    "employee_prog_code": f"Vacancy Vacancy ({vacancy.programme_code})",
                },
            )
        )

    return rows


def payroll_data_report(request: HttpRequest) -> HttpResponse:
    if not payroll_service.can_access_edit_payroll(request.user):
        raise PermissionDenied

    rows = get_report_data(request.user, request.current_financial_year)

    keys, headers = zip(*PAYROLL_REPORT_FIELDS, strict=False)

    context = {"rows": rows, "keys": keys, "headers": headers}

    return TemplateResponse(request, "payroll/page/payroll_data_report.html", context)


def download_report_csv(request: HttpRequest) -> HttpResponse:
    if not payroll_service.can_access_edit_payroll(request.user):
        raise PermissionDenied

    data = get_report_data(request.user, request.current_financial_year)

    filename = f"payroll_data_report_{dt.datetime.now():%Y%m%d-%H%M%S}.csv"
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

    writer = csv.writer(response)
    writer.writerow([header for _, header in PAYROLL_REPORT_FIELDS])

    for row in data:
        writer.writerow([row[key] for key, _ in PAYROLL_REPORT_FIELDS])

    return response
