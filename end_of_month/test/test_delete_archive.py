from django.test import TestCase

from end_of_month.end_of_month_actions import (
    ArchiveMonthInvalidPeriodError,
    DeleteNonExistingArchiveError,
    delete_end_of_month_archive,
    delete_last_end_of_month_archive,
    end_of_month_archive,
)
from end_of_month.models import (
    EndOfMonthStatus,
)
from end_of_month.test.test_utils import (
    MonthlyFigureSetup,
)

from forecast.models import (
    ForecastMonthlyFigure,
)


class DeleteEndOfMonthArchiveTest(TestCase):
    def setUp(self):
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()

    def test_error_invalid_period(self):
        with self.assertRaises(DeleteNonExistingArchiveError):
            delete_last_end_of_month_archive()
        with self.assertRaises(ArchiveMonthInvalidPeriodError):
            delete_end_of_month_archive(0)
        with self.assertRaises(DeleteNonExistingArchiveError):
            delete_end_of_month_archive(1)

    def test_delete_latest_period(self):
        initial_forecast_count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(initial_forecast_count, 15)
        end_of_month_archive(1)
        forecast_count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(forecast_count, 30)
        delete_last_end_of_month_archive()
        forecast_count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(forecast_count, initial_forecast_count)

    def test_delete_selected_period(self):
        end_of_month_archive(1)
        initial_forecast_count = ForecastMonthlyFigure.objects.all().count()
        end_of_month_archive(2)
        end_of_month_obj = EndOfMonthStatus.objects.get(archived_period=2)
        self.assertEqual(end_of_month_obj.archived, True)
        forecast_count = ForecastMonthlyFigure.objects.all().count()
        self.assertNotEqual(forecast_count, initial_forecast_count)
        delete_end_of_month_archive(2)
        forecast_count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(forecast_count, initial_forecast_count)
        end_of_month_obj = EndOfMonthStatus.objects.get(archived_period=2)
        self.assertEqual(end_of_month_obj.archived, False)
