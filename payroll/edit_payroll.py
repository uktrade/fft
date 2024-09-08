import json
import logging

from django.core.serializers import serialize
from django.views.generic.base import TemplateView
from rest_framework import serializers
from rest_framework.response import Response

from costcentre.models import CostCentre
from forecast.views.base import (
    CostCentrePermissionTest,
)
from payroll.models import Payroll, EmployeePayroll
from payroll.serialisers import PayrollSerializer

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

    def get_payroll_serialiser(self):
        get_all_employee_data = EmployeePayroll.objects.all()
        payroll_serialiser = PayrollSerializer(get_all_employee_data, many=True)
        return payroll_serialiser


    def get_context_data(self, **kwargs):
        payroll_serialiser = self.get_payroll_serialiser()
        serialiser_data = payroll_serialiser.data
        payroll_data = json.dumps(serialiser_data)

        self.title = "Edit payroll forecast"
        context = super().get_context_data(**kwargs)
        context['payroll_data'] = payroll_data
        return context


class ErrorView(
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        return 1 / 0
