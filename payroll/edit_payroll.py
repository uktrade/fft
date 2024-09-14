import json
import logging

from django.db import transaction
from django.http import JsonResponse
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from costcentre.models import CostCentre
from forecast.views.base import (
    CostCentrePermissionTest, NoCostCentreCodeInURLError,
)
from payroll.forms import PasteHRForm
from payroll.models import EmployeePayroll, NonEmployeePayroll
from payroll.serialisers import EmployeePayrollSerializer, EmployeeMonthlyPayrollSerializer, \
    NonEmployeePayrollSerializer, NonEmployeeMonthlyPayrollSerializer

logger = logging.getLogger(__name__)

class EditPayrollUpdatesView(
    CostCentrePermissionTest,
    FormView,
):
    form_class = PasteHRForm

    @transaction.atomic
    def form_valid(self, form):  # noqa: C901
        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("no cost centre code provided in URL")

        try:
            cost_centre_code = self.kwargs["cost_centre_code"]
            paste_content = form.cleaned_data["paste_content"]
            pasted_at_row = form.cleaned_data.get("pasted_at_row", None)
            all_selected = form.cleaned_data.get("all_selected", False)

            logger.info(f"cost_centre_code: {cost_centre_code}")
            logger.info(f"paste_content: {paste_content}")
            logger.info(f"pasted_at_row: {pasted_at_row}")
            logger.info(f"all_selected: {all_selected}")
            return JsonResponse({"status": "success"})
        except Exception as e:
            logger.error(f"error parsing form data: {e}")
            return self.form_invalid(form)

class EditPayrollView(
    CostCentrePermissionTest,
    TemplateView,
):
    template_name = "payroll/edit/edit.html"

    def class_name(self):
        return "wide-table"

    def cost_centre_details(self):
        cost_centre = CostCentre.objects.get(
            cost_centre_code=self.cost_centre_code,
        )
        return {
            "group": cost_centre.directorate.group.group_name,
            "group_code": cost_centre.directorate.group.group_code,
            "directorate": cost_centre.directorate.directorate_name,
            "directorate_code": cost_centre.directorate.directorate_code,
            "cost_centre_name": cost_centre.cost_centre_name,
            "cost_centre_code": cost_centre.cost_centre_code,
        }

    def get_employee_payroll_serialiser(self):
        get_all_employee_data = EmployeePayroll.objects.all()
        payroll_serialiser = EmployeePayrollSerializer(get_all_employee_data, many=True)
        return payroll_serialiser

    def get_employee_payroll_monthly_serialiser(self):
        get_all_employee_data = EmployeePayroll.objects.all()
        payroll_monthly_serialiser = EmployeeMonthlyPayrollSerializer(get_all_employee_data, many=True)
        return payroll_monthly_serialiser

    def get_non_employee_payroll_serialiser(self):
        get_all_non_employee_data = NonEmployeePayroll.objects.all()
        non_payroll_serialiser = NonEmployeePayrollSerializer(get_all_non_employee_data, many=True)
        return non_payroll_serialiser

    def get_non_employee_payroll_monthly_serialiser(self):
        get_all_non_employee_data = NonEmployeePayroll.objects.all()
        non_payroll_monthly_serialiser = NonEmployeeMonthlyPayrollSerializer(get_all_non_employee_data, many=True)
        return non_payroll_monthly_serialiser

    def get_context_data(self, **kwargs):
        employee_payroll_serialiser = self.get_employee_payroll_serialiser()
        employee_payroll_serialiser_data = employee_payroll_serialiser.data
        employee_payroll_data = json.dumps(employee_payroll_serialiser_data)

        employee_payroll_monthly_serialiser = self.get_employee_payroll_monthly_serialiser()
        employee_payroll_monthly_serialiser_data = employee_payroll_monthly_serialiser.data
        employee_payroll_monthly_data = json.dumps(employee_payroll_monthly_serialiser_data)

        non_employee_payroll_serialiser = self.get_non_employee_payroll_serialiser()
        non_employee_payroll_serialiser_data = non_employee_payroll_serialiser.data
        non_employee_payroll_data = json.dumps(non_employee_payroll_serialiser_data)

        non_employee_payroll_monthly_serialiser = self.get_non_employee_payroll_monthly_serialiser()
        non_employee_payroll_monthly_serialiser_data = non_employee_payroll_monthly_serialiser.data
        non_employee_payroll_monthly_data = json.dumps(non_employee_payroll_monthly_serialiser_data)

        self.title = "Edit payroll forecast"
        paste_form = PasteHRForm()

        context = super().get_context_data(**kwargs)
        context["paste_form"] = paste_form
        context['payroll_employee_data'] = employee_payroll_data
        context['payroll_employee_monthly_data'] = employee_payroll_monthly_data
        context['payroll_non_employee_data'] = non_employee_payroll_data
        context['payroll_non_employee_monthly_data'] = non_employee_payroll_monthly_data
        return context


class ErrorView(
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        return 1 / 0
