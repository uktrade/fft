import json
import logging

from django.views.generic.base import TemplateView

from costcentre.models import CostCentre
from forecast.views.base import (
    CostCentrePermissionTest,
)
from payroll.models import EmployeePayroll
from payroll.serialisers import EmployeePayrollSerializer, EmployeeMonthlyPayrollSerializer

logger = logging.getLogger(__name__)


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

    def get_context_data(self, **kwargs):
        employee_payroll_serialiser = self.get_employee_payroll_serialiser()
        employee_payroll_serialiser_data = employee_payroll_serialiser.data
        employee_payroll_data = json.dumps(employee_payroll_serialiser_data)

        employee_payroll_monthly_serialiser = self.get_employee_payroll_monthly_serialiser()
        employee_payroll_monthly_serialiser_data = employee_payroll_monthly_serialiser.data
        employee_payroll_monthly_data = json.dumps(employee_payroll_monthly_serialiser_data)


        self.title = "Edit payroll forecast"
        context = super().get_context_data(**kwargs)
        context['payroll_data'] = employee_payroll_data
        context['payroll_monthly_data'] = employee_payroll_monthly_data
        return context


class ErrorView(
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        return 1 / 0
