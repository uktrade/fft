from io import StringIO

from django.test import TestCase
from django.test.utils import captured_stdin
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from core.utils.generic_helpers import get_current_financial_year

from end_of_month.test.test_utils import MonthlyFigureSetup

from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    ForecastMonthlyFigure,
)

from costcentre.models import (
    ArchivedCostCentre,
    CostCentre,
)


class NewFinancialYearTest(TestCase):
    def setUp(self):
        self.out = StringIO()
        init_data = MonthlyFigureSetup()
        init_data.setup_forecast()
        init_data.setup_budget()
        self.current_year = get_current_financial_year()

    def checks_before_command(self):
        assert (
            BudgetMonthlyFigure.objects.filter(financial_year=self.current_year).count()
            != 0
        )
        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count()
            != 0
        )
        assert FinancialCode.objects.all().count() != 0
        assert CostCentre.objects.all().count() != 0
        assert (
            ArchivedCostCentre.objects.filter(financial_year=self.current_year).count()
            == 0
        )

    def check_after_failed_command(self):
        self.checks_before_command()
        current_year_after_command = get_current_financial_year()
        assert current_year_after_command == self.current_year

    def check_after_successfull_command(self):
        assert (
            BudgetMonthlyFigure.objects.filter(financial_year=self.current_year).count()
            == 0
        )
        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count()
            == 0
        )
        assert FinancialCode.objects.all().count() == 0
        assert CostCentre.objects.all().count() != 0
        assert (
            ArchivedCostCentre.objects.filter(financial_year=self.current_year).count()
            != 0
        )
        current_year_after_command = get_current_financial_year()
        assert current_year_after_command != self.current_year

    def create_user(self, is_super_user=False):
        self.user_email = "test@test.com"
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.user_email, is_superuser=is_super_user
        )

    def test_no_permission(self):
        self.checks_before_command()
        self.create_user(False)
        with self.assertRaises(CommandError):
            call_command("new_financial_year", "--useremail", f"{self.user_email}")
        # Check that nothing has changed
        self.check_after_failed_command()

    def test_unknown_user(self):
        self.checks_before_command()
        with self.assertRaises(CommandError):
            call_command("new_financial_year", "--useremail", "Unknown")
        # Check that nothing has changed
        self.check_after_failed_command()

    def test_user_no_answer(self):
        self.checks_before_command()
        self.create_user(True)
        with captured_stdin() as stdin:
            stdin.write("n\n")
            stdin.seek(0)
            with self.assertRaises(CommandError):
                call_command("new_financial_year", "--useremail", f"{self.user_email}")

        # Check that nothing has changed
        self.check_after_failed_command()

    def test_user_yes_answer(self):
        self.checks_before_command()
        self.create_user(True)
        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.seek(0)
            call_command("new_financial_year", "--useremail", f"{self.user_email}")
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
