import pytest
from django.test import TestCase

from core.utils.generic_helpers import get_current_financial_year
from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.test.test_end_of_month_process import (
    TestReadArchivedForecast as BaseTestReadArchivedForecast,
)
from end_of_month.test.test_utils import MonthlyFigureSetup
from forecast.models import ForecastMonthlyFigure


class TestReadArchivedFutureDataForecast(BaseTestReadArchivedForecast):
    @pytest.fixture(autouse=True)
    def _setup(self, db):
        self.archived_figure = [0 for _ in range(16)]
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()
        current_year = get_current_financial_year()
        # Create a set of future forecast data
        self.init_data.set_year(current_year + 2)
        self.init_data.setup_forecast()
        self.init_data.set_year(current_year)


class EndOfMonthFutureDataForecastTest(TestCase):
    def setUp(self):
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()
        self.current_year = get_current_financial_year()
        self.future_year = self.current_year + 2
        # Create data for future forecasts
        self.init_data.set_year(self.future_year)
        self.init_data.setup_forecast()
        self.count_future_year = ForecastMonthlyFigure.objects.filter(
            financial_year_id=self.future_year
        ).count()

    # The following tests that all the periods in the future data are archived
    def check_period(self, period):
        archived_count = 0
        for month in range(0, period):
            archived_count += 15 - month
            end_of_month_archive(month + 1)
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.future_year,
                archived_status__isnull=True,
            ).count(),
            self.count_future_year,
        )

        count_archived_figures = ForecastMonthlyFigure.objects.filter(
            archived_status__isnull=False,
            financial_year_id=self.current_year,
        ).count()
        self.assertEqual(count_archived_figures, archived_count)

        count_future_archived_figures = ForecastMonthlyFigure.objects.filter(
            archived_status__isnull=False,
            financial_year_id=self.future_year,
        ).count()
        self.assertEqual(count_future_archived_figures, period * 15)

    def test_end_of_month_apr(self):
        self.check_period(1)

    def test_end_of_month_may(self):
        self.check_period(2)

    def test_end_of_month_jun(self):
        self.check_period(3)

    def test_end_of_month_jul(self):
        self.check_period(4)

    def test_end_of_month_aug(self):
        self.check_period(5)

    def test_end_of_month_sep(self):
        self.check_period(6)

    def test_end_of_month_oct(self):
        self.check_period(7)

    def test_end_of_month_nov(self):
        self.check_period(8)

    def test_end_of_month_dec(self):
        self.check_period(9)

    def test_end_of_month_jan(self):
        self.check_period(10)

    def test_end_of_month_feb(self):
        self.check_period(11)

    def test_end_of_month_mar(self):
        self.check_period(12)
