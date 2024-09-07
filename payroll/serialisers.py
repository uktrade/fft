from payroll.models import Payroll
from rest_framework import serializers


class PayrollEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = [
            "business_unit_number",
            "business_unit_name",
            "cost_center_number",
            "cost_center_name",
            "employee_name",
            "employee_number",
            "assignment_number",
            "payroll_name",
            "employee_organization",
            "employee_location",
            "person_type",
            "employee_category",
            "assignment_type",
            "position",
            "grade",
            "account_code",
            "account_name",
            "pay_element_name",
            "effective_date",
            "debit_amount",
            "credit_amount",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
            "jan",
            "feb",
            "mar",
        ]
        read_only_fields = fields
