from unittest.mock import patch

import pytest
from pytest_django.asserts import assertNumQueries

from core.test.factories import FinancialYearFactory
from forecast.models import FinancialCode, ForecastMonthlyFigure
from forecast.services import FinancialCodeForecastService
from forecast.test.factories import FinancialCodeFactory, FinancialPeriodFactory


class TestFinancialCodeForecastService:
    @pytest.fixture(autouse=True)
    def _setup(self, db):
        self.code = FinancialCodeFactory()
        self.year = FinancialYearFactory(financial_year=2020)
        self.service = FinancialCodeForecastService(
            financial_code=self.code, year=self.year
        )

    @pytest.fixture
    def period(self, db):
        return FinancialPeriodFactory()

    def test_update_period_creates(self, period):
        with assertNumQueries(6):
            self.service.update_period(period=period, amount=99)

        assert (
            ForecastMonthlyFigure.objects.get(
                financial_code=self.code,
                financial_year=self.year,
                financial_period=period,
                archived_status=None,
            ).amount
            == 99
        )

    def test_update_period_updates(self, period):
        self.service.update_period(period=period, amount=0)

        with assertNumQueries(3):
            self.service.update_period(period=period, amount=99)

        assert (
            ForecastMonthlyFigure.objects.get(
                financial_code=self.code,
                financial_year=self.year,
                financial_period=period,
                archived_status=None,
            ).amount
            == 99
        )

    def test_update_period_ignores_actual(self, period):
        self.service.update_period(period=period, amount=0)

        period.actual_loaded = True
        period.save()

        with assertNumQueries(0):
            self.service.update_period(period=period, amount=99)

        # no change
        assert (
            ForecastMonthlyFigure.objects.get(
                financial_code=self.code,
                financial_year=self.year,
                financial_period=period,
                archived_status=None,
            ).amount
            == 0
        )

    def test_update_period_ignores_locked(self, period, settings):
        self.service.update_period(period=period, amount=0)

        with patch.object(FinancialCode, "is_locked", return_value=True):
            with assertNumQueries(0):
                self.service.update_period(period=period, amount=99)

        # no change
        assert (
            ForecastMonthlyFigure.objects.get(
                financial_code=self.code,
                financial_year=self.year,
                financial_period=period,
                archived_status=None,
            ).amount
            == 0
        )

    def test_update(self, settings):
        forecast = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        self.service.update(forecast)

        for i, x in enumerate(forecast):
            period = i + 1

            assert (
                ForecastMonthlyFigure.objects.get(
                    financial_code=self.code,
                    financial_year=self.year,
                    financial_period_id=period,
                    archived_status=None,
                ).amount
                == x
            )
