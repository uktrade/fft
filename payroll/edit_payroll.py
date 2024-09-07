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
from payroll.models import Payroll

logger = logging.getLogger(__name__)


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ['payroll_id', 'created_at', 'business_unit_number', 'business_unit_name', 'cost_center_number', 'cost_center_name', 'employee_name', 'employee_number', 'assignment_number', 'payroll_name', 'employee_organization', 'employee_location', 'person_type', 'employee_category', 'assignment_type', 'position', 'grade', 'account_code', 'account_name', 'pay_element_name', 'effective_date', 'debit_amount', 'credit_amount']


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

    def get_payroll_data(self):
        # Fetch payroll data logic here
        payroll_data = list(Payroll.objects.all().values())
        return payroll_data


    def get_context_data(self, **kwargs):
        self.title = "Edit payroll forecast"
        context = super().get_context_data(**kwargs)
        context['payroll_data'] = self.get_payroll_data()
        return context


class ErrorView(
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        return 1 / 0
