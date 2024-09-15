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
            paste_content = form.clean_pasted_at_row()
            staff_employee = paste_content["staff_number"][0]
            month_name = paste_content["month"][0]
            amount_value = paste_content["amount"][0]
            table = paste_content["table"][0]

            logger.info(f"cost_centre_code: {cost_centre_code}")
            logger.info(f"paste_content: {paste_content}")
            logger.info(f"month name: {month_name}")
            logger.info(f"amount value: {amount_value}")
            logger.info(f"staff_employee: {staff_employee}")
            logger.info(f"table: {table}")

            # get the first item from the list from table data
            if table == "non_payroll":
                non_employee_payroll = NonEmployeePayroll.objects.get(
                    staff_number=staff_employee,
                    # cost_centre_code=cost_centre_code,
                )
                if month_name == "jan":
                    non_employee_payroll.jan = int(amount_value)
                if month_name == "feb":
                    non_employee_payroll.feb = int(amount_value)
                if month_name == "mar":
                    non_employee_payroll.mar = int(amount_value)
                if month_name == "apr":
                    non_employee_payroll.apr = int(amount_value)
                if month_name == "may":
                    non_employee_payroll.may = int(amount_value)
                if month_name == "jun":
                    non_employee_payroll.jun = int(amount_value)
                if month_name == "jul":
                    non_employee_payroll.jul = int(amount_value)
                if month_name == "aug":
                    non_employee_payroll.aug = int(amount_value)
                if month_name == "sep":
                    non_employee_payroll.sep = int(amount_value)
                if month_name == "oct":
                    non_employee_payroll.oct = int(amount_value)
                if month_name == "nov":
                    non_employee_payroll.nov = int(amount_value)
                if month_name == "dec":
                    non_employee_payroll.dec = int(amount_value)

                non_employee_payroll.save()
            else:
                employee_payroll = EmployeePayroll.objects.get(
                    staff_number=staff_employee,
                    # cost_centre_code=cost_centre_code,
                )
                if month_name == "jan":
                    employee_payroll.jan = int(amount_value)
                if month_name == "feb":
                    employee_payroll.feb = int(amount_value)
                if month_name == "mar":
                    employee_payroll.mar = int(amount_value)
                if month_name == "apr":
                    employee_payroll.apr = int(amount_value)
                if month_name == "may":
                    employee_payroll.may = int(amount_value)
                if month_name == "jun":
                    employee_payroll.jun = int(amount_value)
                if month_name == "jul":
                    employee_payroll.jul = int(amount_value)
                if month_name == "aug":
                    employee_payroll.aug = int(amount_value)
                if month_name == "sep":
                    employee_payroll.sep = int(amount_value)
                if month_name == "oct":
                    employee_payroll.oct = int(amount_value)
                if month_name == "nov":
                    employee_payroll.nov = int(amount_value)
                if month_name == "dec":
                    employee_payroll.dec = int(amount_value)

                employee_payroll.save()

            if table == "non_payroll":
                get_all_non_employee_data = NonEmployeePayroll.objects.all()
                non_payroll_monthly_serialiser = NonEmployeeMonthlyPayrollSerializer(get_all_non_employee_data, many=True)
                non_payroll_serialiser = NonEmployeePayrollSerializer(get_all_non_employee_data, many=True)

                return JsonResponse({
                    "month": non_payroll_monthly_serialiser.data,
                    "payroll": non_payroll_serialiser.data
                })
            else:
                get_all_employee_data = EmployeePayroll.objects.all()
                payroll_monthly_serialiser = EmployeeMonthlyPayrollSerializer(get_all_employee_data, many=True)
                payroll_serialiser = EmployeePayrollSerializer(get_all_employee_data, many=True)

                return JsonResponse({
                    "month": payroll_monthly_serialiser.data,
                    "payroll": payroll_serialiser.data
                })

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
