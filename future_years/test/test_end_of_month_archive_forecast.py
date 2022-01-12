from django.test import TestCase

from core.utils.generic_helpers import get_current_financial_year

from end_of_month.end_of_month_actions import (
    end_of_month_archive,
)
from end_of_month.test.test_end_of_month_process import ReadArchivedForecastTest
from end_of_month.test.test_utils import (
    MonthlyFigureSetup,
)

from forecast.models import (
    ForecastMonthlyFigure,
)


class ReadArchivedFutureDataForecast(ReadArchivedForecastTest):
    def setUp(self):
        super().setUp()
        current_year = get_current_financial_year()
        # Create a set of data for the future
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

    # The following tests that no future data is archived
    def check_period(self, period):
        archived_count = 0
        for month in range(0, period):
            archived_count += 15 - month
            end_of_month_archive(month + 1)
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.future_year
            ).count(),
            self.count_future_year,
        )
        count_archived_figures = ForecastMonthlyFigure.objects.filter(
            archived_status__isnull=False
        ).count()
        self.assertEqual(count_archived_figures, archived_count)

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
