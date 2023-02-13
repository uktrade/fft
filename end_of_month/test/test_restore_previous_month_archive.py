from django.test import TestCase

from end_of_month.end_of_month_actions import RestoreNonExistingArchiveError
from end_of_month.models import EndOfMonthStatus
from end_of_month.restore_archive import restore_archive
from end_of_month.test.test_utils import SetFullYearArchive
from forecast.models import ForecastMonthlyFigure


class RestoreArchiveTest(TestCase):
    def setUp(self):
        self.restore_period = 8
        self.archive = SetFullYearArchive(self.restore_period + 1)

    def test_error_invalid_period(self):
        with self.assertRaises(RestoreNonExistingArchiveError):
            restore_archive(self.restore_period + 1)

    def test_delete_selected_period(self):
        initial_forecast_count = ForecastMonthlyFigure.objects.all().count()
        restore_archive(self.restore_period)
        end_of_month_obj = EndOfMonthStatus.objects.get(
            archived_period=self.restore_period
        )
        self.assertEqual(end_of_month_obj.archived, False)
        forecast_count = ForecastMonthlyFigure.objects.all().count()
        self.assertNotEqual(forecast_count, initial_forecast_count)
