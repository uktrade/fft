import os
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Sum
from django.test import TestCase
from django.test.utils import captured_stdin

from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year
from forecast.models import BudgetMonthlyFigure, FinancialPeriod, ForecastMonthlyFigure
from future_years.test.future_year_utils import FutureFigureSetup


TOTAL_FROM_FILE = 85800000


def year_forecast_total(year):
    query = ForecastMonthlyFigure.objects.filter(financial_year=year).aggregate(
        total_for_year=Sum("amount")
    )
    return query["total_for_year"]


class ImportFutureForecastTest(TestCase):
    def setUp(self):
        self.current_year = get_current_financial_year()
        self.test_year = self.current_year + 2
        self.out = StringIO()
        self.init_data = FutureFigureSetup(self.test_year)
        self.path = (
            os.path.join(
                os.path.dirname(__file__),
                "test_assets/forecast_upload_test.xlsx",
            ),
        )

    def test_no_answer(self):
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        with captured_stdin() as stdin:
            stdin.write("n\n")
            stdin.seek(0)
            with self.assertRaises(CommandError):
                call_command("upload_future_year_forecast", self.path, self.test_year)
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )

    def test_wrong_year(self):
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.seek(0)
            with self.assertRaises(CommandError):
                call_command(
                    "upload_future_year_forecast", self.path, self.current_year
                )
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )

    def test_no_previous_data(self):
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.seek(0)
            call_command("upload_future_year_forecast", self.path, self.test_year)
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            12,
        )
        self.assertEqual(TOTAL_FROM_FILE, year_forecast_total(self.test_year))

    def test_with_data_in_future_year(self):
        self.init_data.setup_forecast(True)
        previous_total = year_forecast_total(self.test_year)
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.seek(0)
            call_command("upload_future_year_forecast", self.path, self.test_year)
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        self.assertNotEqual(previous_total, year_forecast_total(self.test_year))
        self.assertEqual(TOTAL_FROM_FILE, year_forecast_total(self.test_year))

    def test_with_data_in_current_year(self):
        # Create data in the current year
        self.init_data.setup_forecast(False)
        previous_total = year_forecast_total(self.current_year)
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.seek(0)
            call_command("upload_future_year_forecast", self.path, self.test_year)
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        # The current year data has not been changed
        self.assertEqual(previous_total, year_forecast_total(self.current_year))
        self.assertEqual(TOTAL_FROM_FILE, year_forecast_total(self.test_year))

    def test_with_actuals(self):
        # Create data in the current year
        self.init_data.setup_forecast(False)
        previous_total = year_forecast_total(self.current_year)
        FinancialPeriod.objects.filter(financial_period_code=1).update(
            actual_loaded=True
        )
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.seek(0)
            call_command("upload_future_year_forecast", self.path, self.test_year)
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        # The current year data has not been changed
        self.assertEqual(previous_total, year_forecast_total(self.current_year))
        self.assertEqual(TOTAL_FROM_FILE, year_forecast_total(self.test_year))

    def test_year_created(self):
        # Check that the test year does not exist
        assert FinancialYear.objects.filter(financial_year=self.test_year).count() == 0

        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.seek(0)
            call_command("upload_future_year_forecast", self.path, self.test_year)

        # Check that the test year does not exist
        assert FinancialYear.objects.filter(financial_year=self.test_year).count() == 1
