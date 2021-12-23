from io import StringIO

from django.test import TestCase
from django.test.utils import captured_stdin
from django.core.management import call_command
from django.core.management.base import CommandError

from core.utils.generic_helpers import get_current_financial_year

from future_years.test.future_year_utils import FutureFigureSetup

from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    ForecastMonthlyFigure,
)


class ImportFutureForecastTest(TestCase):
    def setUp(self):
        self.current_year = get_current_financial_year()
        self.test_year = self.current_year + 2
        self.out = StringIO()
        self.init_data = FutureFigureSetup(self.test_year)

    def test_no_answer(self):
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year
            ).count(),
            0,
        )
        self.assertNotEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_year=self.test_year
            ).count(),
            0,
        )
        path = ""
        with captured_stdin() as stdin:
            stdin.write("n\n")
            stdin.seek(0)
            with self.assertRaises(CommandError):
                call_command(
                    "upload_future_year_forecast",
                    path,
                    self.test_year)
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year
            ).count(),
            0,
        )
        self.assertNotEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_year=self.test_year
            ).count(),
            0,
        )
