from io import StringIO

from django.test import TestCase
from django.test.utils import captured_stdin
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

    def test_no_answer(self):
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

        with captured_stdin() as stdin:
            stdin.write("n\n")
            stdin.seek(0)
            with self.assertRaises(CommandError):
                call_command("new_financial_year")

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
        assert ArchivedCostCentre.objects.all().count() == 0
        assert CostCentre.objects.all().count() != 0
        assert (
            ArchivedCostCentre.objects.filter(financial_year=self.current_year).count()
            == 0
        )

        current_year_after_command = get_current_financial_year()
        assert current_year_after_command == self.current_year

    def test_yes_answer(self):
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

        with captured_stdin() as stdin:
            stdin.write("y\n")
            stdin.seek(0)
            call_command("new_financial_year")
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.current_year
            ).count(),
            0,
        )
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
