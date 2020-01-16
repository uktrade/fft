from rest_framework import serializers

from .models import (
    FinancialCode,
    ForecastMonthlyFigure,
)


class ForecastMonthlyFigureSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField('get_month')
    actual = serializers.SerializerMethodField('get_actual')

    class Meta:
        model = ForecastMonthlyFigure
        fields = [
            'actual',
            'month',
            'amount',
        ]
        read_only_fields = fields

    def get_month(self, obj):
        return obj.financial_period.financial_period_code

    def get_actual(self, obj):
        return obj.financial_period.actual_loaded


class FinancialCodeSerializer(serializers.ModelSerializer):
    monthly_figures = ForecastMonthlyFigureSerializer(
        many=True,
        read_only=True,
        source='forecast_forecastmonthlyfigures',
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
