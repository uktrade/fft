from unittest.mock import patch

import pytest
from pytest_django.asserts import assertNumQueries

from core.models import FinancialYear
from core.test.factories import FinancialYearFactory
from forecast.models import FinancialCode, ForecastMonthlyFigure
from forecast.services import (
    FinancialCodeForecastService,
    get_forecast_periods_for_year,
)
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


@pytest.mark.parametrize(
    ["year", "forecast_periods"],
    [
        [2019, []],
        [2020, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]],
        [2021, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]],
    ],
)
def test_get_forecast_periods_for_year(db, year: int, forecast_periods: list[int]):
    FinancialYearFactory(financial_year=2019, current=False)
    FinancialYearFactory(financial_year=2020, current=True)
    FinancialYearFactory(financial_year=2021, current=False)

    actual_periods = [
        FinancialPeriodFactory(financial_period_code=1),
        FinancialPeriodFactory(financial_period_code=2),
    ]
    for period in actual_periods:
        period.actual_loaded = True
        period.save()

    year_obj = FinancialYear.objects.get(financial_year=year)
    forecast_period_objs = list(get_forecast_periods_for_year(year_obj))

    assert [obj.pk for obj in forecast_period_objs] == forecast_periods
