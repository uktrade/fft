from rest_framework import serializers

from payroll.models import EmployeePayroll, NonEmployeePayroll


class EmployeeMonthlyPayrollSerializer(serializers.ModelSerializer):
    """
    Serializer for EmployeeMonthlyPayroll to serialize and deserialize
    EmployeePayroll model data for each month.

       class EmployeeMonthlyPayrollSerializer(serializers.ModelSerializer):
           class Meta:
               model = EmployeePayroll
               fields = [
                   "apr", "may", "jun", "jul", "aug", "sep",
                   "oct", "nov", "dec", "jan", "feb", "mar"
               ]
               read_only_fields = fields
    """
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
    """
    Serializer for EmployeePayroll model.

    Attributes:
        Meta (class): Meta options for the EmployeePayrollSerializer.
            model (EmployeePayroll): Specifies the model to be serialized.
            fields (list): List of fields to be included in the serialization.
            read_only_fields (list): List of fields that should be read-only.
    """
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


class NonEmployeeMonthlyPayrollSerializer(serializers.ModelSerializer):
    """
        NonEmployeeMonthlyPayrollSerializer is a ModelSerializer for the NonEmployeePayroll model.

        Meta class:

        - model: Specifies the model to be serialized, which is NonEmployeePayroll.

        - fields: Lists the fields to be included in the serialization. These fields represent the months of the fiscal year:
            - "apr"
            - "may"
            - "jun"
            - "jul"
            - "aug"
            - "sep"
            - "oct"
            - "nov"
            - "dec"
            - "jan"
            - "feb"
            - "mar"

        - read_only_fields: Specifies the fields that are read-only. In this case, all fields listed in 'fields' are set to read-only.
    """
    class Meta:
        model = NonEmployeePayroll
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


class NonEmployeePayrollSerializer(serializers.ModelSerializer):
    """
        NonEmployeePayrollSerializer is a ModelSerializer for the NonEmployeePayroll model.

        class Meta:
            - model: Specifies the model to be serialized, which is NonEmployeePayroll.
            - fields: Lists the fields to be included in the serialization. These are:
                - name
                - grade
                - staff_number
                - fte
                - programme_code
                - budget_type
                - eu_non_eu
                - assignment_status
            - read_only_fields: Specifies the fields to be treated as read-only. In this case, it is set to the same fields listed in 'fields'.
    """
    class Meta:
        model = NonEmployeePayroll
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