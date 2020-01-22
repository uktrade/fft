from django.db.models import (
    Sum,
)

from rest_framework import serializers

from core.myutils import get_current_financial_year

from .models import (
    BudgetMonthlyFigure,
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
            'starting_amount',
        ]
        read_only_fields = fields

    def get_month(self, obj):
        return obj.financial_period.financial_period_code

    def get_actual(self, obj):
        return obj.financial_period.actual_loaded


class FinancialCodeSerializer(serializers.ModelSerializer):
    budget = serializers.SerializerMethodField('get_budget')
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
            'budget',
        ]
        read_only_fields = fields

    def get_budget(self, obj):
        budget = BudgetMonthlyFigure.objects.values(
            'financial_code',
            'financial_year',
        ).filter(
            financial_code=obj.id,
            financial_year_id=get_current_financial_year(),
        ).annotate(
            yearly_amount=Sum('amount')
        )

        if budget and "yearly_amount" in budget[0]:
            return budget[0]["yearly_amount"]
        else:
            return 0
