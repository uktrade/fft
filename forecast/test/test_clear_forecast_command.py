from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.test.utils import captured_stdin

from core.utils.generic_helpers import get_current_financial_year
from end_of_month.test.test_utils import MonthlyFigureSetup
from forecast.models import BudgetMonthlyFigure, FinancialCode, ForecastMonthlyFigure


class ClearForecastCommandNoArchiveTest(TestCase):
    def setUp(self):
        init_data = MonthlyFigureSetup()
        init_data.setup_forecast()
        init_data.setup_budget()
        self.current_year = get_current_financial_year()

    def assertFiguresCount(self, should_exist=True):
        count_assert = self.assertNotEqual if should_exist else self.assertEqual
        count_assert(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
        count_assert(
            ForecastMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
        count_assert(FinancialCode.objects.all().count(), 0)

    def test_no_answer(self):
        self.assertFiguresCount()
        with captured_stdin() as stdin:
            stdin.write("n\n")
            stdin.seek(0)
            with self.assertRaises(CommandError):
                call_command("clear_forecast")
        self.assertFiguresCount()

    def test_yes_no_answer(self):
        self.assertFiguresCount()
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.write("n")
            stdin.seek(0)
            with self.assertRaises(CommandError):
                call_command("clear_forecast")
        self.assertFiguresCount()

    def test_yes_yes_answer(self):
        self.assertFiguresCount()
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.write("y")
            stdin.seek(0)
            call_command("clear_forecast")
        self.assertFiguresCount(False)

    def test_not_interactive(self):
        self.assertFiguresCount()
        with self.assertRaises(CommandError):
            call_command("clear_forecast", "--noinput")
        self.assertFiguresCount()


class ClearForecastCommandWithArchiveTest(TestCase):
    def setUp(self):
        init_data = MonthlyFigureSetup()
        init_data.setup_forecast()
        init_data.setup_budget()
        call_command("archive")
        self.current_year = get_current_financial_year()
        call_command(
            "archive_current_year",
        )

    def assertFiguresCount(self, should_exist=True):
        count_assert = self.assertNotEqual if should_exist else self.assertEqual
        count_assert(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
        count_assert(
            ForecastMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
        count_assert(FinancialCode.objects.all().count(), 0)

    def test_no_answer(self):
        self.assertFiguresCount()
        with captured_stdin() as stdin:
            stdin.write("n\n")
            stdin.seek(0)
            with self.assertRaises(CommandError):
                call_command("clear_forecast")
        self.assertFiguresCount()

    def test_yes_answer(self):
        self.assertFiguresCount()
        with captured_stdin() as stdin:
            stdin.write("y")
            stdin.seek(0)
            call_command("clear_forecast")
        self.assertFiguresCount(False)

    def test_not_interactive(self):
        self.assertFiguresCount()
        call_command("clear_forecast", "--noinput")
        self.assertFiguresCount(False)
