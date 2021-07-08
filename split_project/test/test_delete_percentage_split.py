from django.db.models import F
from io import StringIO

from django.core.management import call_command
from django.test import TestCase


from core.utils.generic_helpers import get_current_financial_year

from forecast.models import (
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.test.factories import FinancialCodeFactory

from split_project.models import PaySplitCoefficient


class DeletePercentageSplitCommandTest(TestCase):
    def setUp(self):
        self.out = StringIO()
        FinancialPeriod.objects.all().update(actual_loaded=True)
        self.current_year = get_current_financial_year()
        self.financial_period = 5
        FinancialPeriod.objects.all().update(actual_loaded=True)

        financial_code_obj = FinancialCodeFactory.create()

        ForecastMonthlyFigure.objects.create(
            oracle_amount=12345,
            amount=99999,
            financial_period_id=self.financial_period,
            financial_code=financial_code_obj,
            financial_year_id=self.current_year,
        )

        ForecastMonthlyFigure.objects.create(
            oracle_amount=12345,
            amount=99999,
            financial_period_id=self.financial_period + 1,
            financial_code=financial_code_obj,
            financial_year_id=self.current_year,
        )

        PaySplitCoefficient.objects.create(
            financial_period_id=self.financial_period,
            financial_code_to=financial_code_obj,
            directorate_code="AAAA",
            split_coefficient="2345",
        )
        PaySplitCoefficient.objects.create(
            financial_period_id=self.financial_period + 1,
            financial_code_to=financial_code_obj,
            directorate_code="AAAA",
            split_coefficient="2345",
        )
        self.period_obj = FinancialPeriod.objects.get(
            financial_period_code=self.financial_period
        )

    def test_delete_percentage_split(self):

        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.current_year,
                financial_period_id=self.financial_period,
                archived_status__isnull=True,
                amount=F("oracle_amount"),
            ).count()
            == 0
        )
        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.current_year,
                financial_period_id=self.financial_period + 1,
                archived_status__isnull=True,
                amount=F("oracle_amount"),
            ).count()
            == 0
        )

        assert (
            PaySplitCoefficient.objects.filter(
                financial_period_id=self.financial_period,
            ).count()
            != 0
        )
        assert (
            PaySplitCoefficient.objects.filter(
                financial_period_id=self.financial_period + 1,
            ).count()
            != 0
        )
        call_command(
            "delete_percentage_split", self.financial_period, stdout=self.out,
        )

        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.current_year,
                financial_period_id=self.financial_period,
                archived_status__isnull=True,
                amount=F("oracle_amount"),
            ).count()
            != 0
        )

        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.current_year,
                financial_period_id=self.financial_period + 1,
                archived_status__isnull=True,
                amount=F("oracle_amount"),
            ).count()
            == 0
        )
        assert (
            PaySplitCoefficient.objects.filter(
                financial_period_id=self.financial_period,
            ).count()
            == 0
        )
        assert (
            PaySplitCoefficient.objects.filter(
                financial_period_id=self.financial_period + 1,
            ).count()
            != 0
        )
