from rest_framework import serializers

from payroll.models import EmployeePayroll


class EmployeeMonthlyPayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePayroll
        fields = [
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


class EmployeePayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePayroll
        fields = [
            "name",
            "grade",
            "staff_number",
            "fte",
            "programme_code",
            "budget_type",
            "eu_non_eu",
            "assignment_status",
        ]
        read_only_fields = fields