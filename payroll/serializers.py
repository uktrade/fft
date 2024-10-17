import re

from rest_framework import serializers

from .models import EmployeePayPeriods


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePayPeriods
        fields = [
            "name",
            "employee_no",
            "period_1",
            "period_2",
            "period_3",
            "period_4",
            "period_5",
            "period_6",
            "period_7",
            "period_8",
            "period_9",
            "period_10",
            "period_11",
            "period_12",
        ]

    name = serializers.CharField(source="employee.get_full_name")
    employee_no = serializers.CharField(source="employee.employee_no")

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        period_field_re = re.compile(r"period_[0-9]{1,2}")
        for key, value in validated_data.items():
            if re.fullmatch(period_field_re, key):
                setattr(instance, key, value)
        instance.save()
        return instance
