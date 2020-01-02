from rest_framework import serializers

from .models import (
    FinancialCode,
    MonthlyFigure,
    MonthlyFigureAmount,
)


class MonthlyFigureAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyFigureAmount
        fields = [
            'amount',
            'version',
        ]
        read_only_fields = fields


class MonthlyFigureSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField('get_month')
    actual = serializers.SerializerMethodField('get_actual')
    monthly_figure_amounts = MonthlyFigureAmountSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = MonthlyFigure
        fields = [
            'actual',
            'month',
            'monthly_figure_amounts',
        ]
        read_only_fields = fields

    def get_month(self, obj):
        return obj.financial_period.period_calendar_code

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
        read_only_fields = fields
