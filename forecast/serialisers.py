from rest_framework import serializers

from .models import (
    FinancialCode,
    MonthlyFigure,
)


class MonthlyFigureSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField('get_month')
    actual = serializers.SerializerMethodField('get_actual')

    class Meta:
        model = MonthlyFigure
        fields = [
            'actual',
            'month',
            'amount',
            'version',
        ]

    def get_month(self, obj):
        return obj.financial_period.period_short_name.lower()

    def get_actual(self, obj):
        return obj.financial_period.actual_loaded


class FinancialCodeSerializer(serializers.ModelSerializer):
    monthly_figures = MonthlyFigureSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = FinancialCode
        fields = [
            'programme',
            'cost_centre',
            'natural_account_code',
            'analysis1_code',
            'analysis2_code',
            'project_code',
            'monthly_figures',
        ]


