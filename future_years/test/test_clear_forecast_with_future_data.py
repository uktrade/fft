from io import StringIO

from django.test import TestCase
from django.test.utils import captured_stdin
from django.core.management import call_command

from core.utils.generic_helpers import get_current_financial_year

from end_of_month.test.test_utils import MonthlyFigureSetup

from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    ForecastMonthlyFigure,
)


class ClearForecastCommandFutureDataTest(TestCase):
    def setUp(self):
        self.out = StringIO()
        init_data = MonthlyFigureSetup()
        init_data.setup_forecast()
        init_data.setup_budget()
        self.current_year = get_current_financial_year()

        init_data.set_year(self.current_year + 1)
        init_data.setup_forecast()
        init_data.setup_budget()

        init_data.set_year(self.current_year + 2)
        init_data.setup_forecast()
        init_data.setup_budget()

    def test_yes_yes_answer(self):
        self.assertNotEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
        self.assertNotEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
        self.assertNotEqual(FinancialCode.objects.all().count(), 0)
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.write("y")
            stdin.seek(0)
            call_command("clear_forecast")
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
        self.assertNotEqual(FinancialCode.objects.all().count(), 0)

        self.assertNotEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.current_year + 1
            ).count(),
            0,
        )

        self.assertNotEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.current_year + 2
            ).count(),
            0,
        )
