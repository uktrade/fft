from django.db.models import Sum
from rest_framework import serializers

from core.utils.generic_helpers import get_current_financial_year

from .models import BudgetMonthlyFigure, FinancialCode, ForecastMonthlyFigure


class ForecastMonthlyFigureSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField("get_month")
    actual = serializers.SerializerMethodField("get_actual")

    class Meta:
        model = ForecastMonthlyFigure
        fields = [
            "actual",
            "month",
            "amount",
            "starting_amount",
            "archived_status",
        ]
        read_only_fields = fields

    def get_month(self, obj):
        return obj.financial_period.financial_period_code

    def get_actual(self, obj):
        if obj.financial_year_id > get_current_financial_year():
            return False
        return obj.financial_period.actual_loaded


class FinancialCodeSerializer(serializers.ModelSerializer):
    budget = serializers.SerializerMethodField("get_budget")
    monthly_figures = ForecastMonthlyFigureSerializer(
        many=True,
        read_only=True,
        source="monthly_figure_items",
    )
    programme_description = serializers.SerializerMethodField(
        "get_programme_description",
    )
    nac_description = serializers.SerializerMethodField(
        "get_nac_description",
    )

    class Meta:
        model = FinancialCode
        fields = [
            "programme_description",
            "nac_description",
            "natural_account_code",
            "programme",
            "cost_centre",
            "analysis1_code",
            "analysis2_code",
            "project_code",
            "monthly_figures",
            "budget",
        ]
        read_only_fields = fields

    def get_programme_description(self, obj):
        return obj.programme.programme_description

    def get_nac_description(self, obj):
        return obj.natural_account_code.natural_account_code_description

    def get_budget(self, obj):
        financial_year = self.context["financial_year"]
        budget = (
            BudgetMonthlyFigure.objects.values(
                "financial_code",
                "financial_year",
            )
            .filter(
                financial_code=obj.id,
                financial_year_id=financial_year,
                archived_status=None,
            )
            .annotate(yearly_amount=Sum("amount"))
        )

        if budget and "yearly_amount" in budget[0]:
            return budget[0]["yearly_amount"]
        else:
            return 0
