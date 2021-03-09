from django.core.management import call_command
from django.core.management.base import CommandError

from django.test import TestCase

from end_of_month.test.test_utils import MonthlyFigureSetup

from previous_years.archive_current_year_figure import archive_current_year

from previous_years.models import (
    ArchivedFinancialCode,
    ArchivedForecastData,
)
from previous_years.utils import ArchiveYearError


class ArchiveCurrentYearErrorTest(TestCase):
    def setUp(self):
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()

    def test_command_error(self):
        with self.assertRaises(CommandError):
            call_command("archive_current_year",)

    def test_error_no_archived_chart_of_account(self):
        with self.assertRaises(ArchiveYearError):
            archive_current_year()


class ArchiveCurrentYearTest(TestCase):
    def setUp(self):
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()
        self.init_data.setup_budget()
        call_command("archive")

    def test_archive_actuals(self):
        self.assertEqual(ArchivedFinancialCode.objects.count(), 0)
        self.assertEqual(ArchivedForecastData.objects.count(), 0)
        call_command("archive_current_year",)
        self.assertEqual(ArchivedFinancialCode.objects.count(), 1)
        self.assertEqual(ArchivedForecastData.objects.count(), 1)
        ArchivedForecastData_obj = ArchivedForecastData.objects.all().first()
        value_dict = self.init_data.value_dict
        self.assertEqual(ArchivedForecastData_obj.apr, value_dict[1])
        self.assertEqual(ArchivedForecastData_obj.may, value_dict[2])
        self.assertEqual(ArchivedForecastData_obj.jun, value_dict[3])
        self.assertEqual(ArchivedForecastData_obj.jul, value_dict[4])
        self.assertEqual(ArchivedForecastData_obj.aug, value_dict[5])
        self.assertEqual(ArchivedForecastData_obj.sep, value_dict[6])
        self.assertEqual(ArchivedForecastData_obj.oct, value_dict[7])
        self.assertEqual(ArchivedForecastData_obj.nov, value_dict[8])
        self.assertEqual(ArchivedForecastData_obj.dec, value_dict[9])
        self.assertEqual(ArchivedForecastData_obj.jan, value_dict[10])
        self.assertEqual(ArchivedForecastData_obj.feb, value_dict[11])
        self.assertEqual(ArchivedForecastData_obj.mar, value_dict[12])
        self.assertEqual(ArchivedForecastData_obj.adj1, value_dict[13])
        self.assertEqual(ArchivedForecastData_obj.adj2, value_dict[14])
        self.assertEqual(ArchivedForecastData_obj.adj3, value_dict[15])

    def test_archive_budget(self):
        self.assertEqual(ArchivedFinancialCode.objects.count(), 0)
        self.assertEqual(ArchivedForecastData.objects.count(), 0)
        call_command("archive_current_year",)
        self.assertEqual(ArchivedFinancialCode.objects.count(), 1)
        self.assertEqual(ArchivedForecastData.objects.count(), 1)
        ArchivedForecastData_obj = ArchivedForecastData.objects.all().first()
        self.assertEqual(ArchivedForecastData_obj.budget, self.init_data.total_budget)
