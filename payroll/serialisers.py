from rest_framework import serializers

from payroll.models import EmployeePayroll


class PayrollSerializer(serializers.ModelSerializer):
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