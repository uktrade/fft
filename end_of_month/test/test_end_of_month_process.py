from django.db.models import F
from django.test import TestCase

from end_of_month.end_of_month_actions import (
    ArchiveMonthAlreadyArchivedError,
    ArchiveMonthArchivedPastError,
    ArchiveMonthInvalidPeriodError,
    end_of_month_archive,
)
from end_of_month.models import (
    MonthlyTotalBudget,
    forecast_budget_view_model,
)
from end_of_month.test.test_utils import (
    MonthlyFigureSetup,
)

from core.test.test_base import RequestFactoryBase

from forecast.models import (
    BudgetMonthlyFigure,
    ForecastMonthlyFigure,
)


class EndOfMonthForecastTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()

    def test_error_invalid_period(self):
        with self.assertRaises(ArchiveMonthInvalidPeriodError):
            end_of_month_archive(16)
        with self.assertRaises(ArchiveMonthInvalidPeriodError):
            end_of_month_archive(0)

    def test_error_already_archived_period(self):
        period = 5
        end_of_month_archive(period)
        with self.assertRaises(ArchiveMonthAlreadyArchivedError):
            end_of_month_archive(period)

    def test_error_early_archived_period(self):
        period = 5
        end_of_month_archive(period)
        with self.assertRaises(ArchiveMonthArchivedPastError):
            end_of_month_archive(period - 1)

    # The following tests test_end_of_month_xxx checkes that only forecast is saved,
    # not actuals. This is tested by counting the records saved in the period tested.
    def test_end_of_month_apr(self):
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 15)
        end_of_month_archive(1)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 30)

    def test_end_of_month_may(self):
        self.test_end_of_month_apr()
        end_of_month_archive(2)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 44)

    def test_end_of_month_jun(self):
        self.test_end_of_month_may()
        end_of_month_archive(3)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 57)

    def test_end_of_month_jul(self):
        self.test_end_of_month_jun()
        end_of_month_archive(4)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 69)

    def test_end_of_month_aug(self):
        self.test_end_of_month_jul()
        end_of_month_archive(5)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 80)

    def test_end_of_month_sep(self):
        self.test_end_of_month_aug()
        end_of_month_archive(6)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 90)

    def test_end_of_month_oct(self):
        self.test_end_of_month_sep()
        end_of_month_archive(7)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 99)

    def test_end_of_month_nov(self):
        self.test_end_of_month_oct()
        end_of_month_archive(8)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 107)

    def test_end_of_month_dec(self):
        self.test_end_of_month_nov()
        end_of_month_archive(9)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 114)

    def test_end_of_month_jan(self):
        self.test_end_of_month_dec()
        end_of_month_archive(10)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 120)

    def test_end_of_month_feb(self):
        self.test_end_of_month_jan()
        end_of_month_archive(11)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 125)

    def test_end_of_month_mar(self):
        self.test_end_of_month_feb()
        end_of_month_archive(12)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 129)


class ReadArchivedForecastTest(TestCase, RequestFactoryBase):
    archived_figure = []

    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()
        for period in range(0, 16):
            self.archived_figure.append(0)

    def get_period_total(self, period):
        data_model = forecast_budget_view_model[period]
        tot_q = data_model.objects.annotate(
            total=F("apr")
            + F("may")
            + F("jun")
            + F("jul")
            + F("aug")
            + F("sep")
            + F("oct")
            + F("nov")
            + F("dec")
            + F("jan")
            + F("feb")
            + F("mar")
            + F("adj1")
            + F("adj2")
            + F("adj3")
        )
        return tot_q[0].total

    def get_current_total(self):
        return self.get_period_total(0)

    def check_archive_period(self, tested_period):
        total_before = self.get_current_total()
        end_of_month_archive(tested_period)
        # run a query giving the full total
        archived_total = self.get_period_total(tested_period)
        self.assertEqual(total_before, archived_total)
        change_amount = tested_period * 10000
        self.init_data.monthly_figure_update(tested_period + 1, change_amount)
        current_total = self.get_current_total()
        self.archived_figure[tested_period] = archived_total
        self.assertNotEqual(current_total, archived_total)
        self.assertEqual(current_total, (archived_total + change_amount))
        for period in range(1, tested_period + 1):
            self.assertEqual(
                self.archived_figure[period], self.get_period_total(period)
            )

    # The following tests check that the archived figures are not changed by
    # changing the current figures.
    def test_read_archived_figure_apr(self):
        tested_period = 1
        self.check_archive_period(tested_period)

    def test_read_archived_figure_may(self):
        tested_period = 2
        self.test_read_archived_figure_apr()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_jun(self):
        tested_period = 3
        self.test_read_archived_figure_may()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_jul(self):
        tested_period = 4
        self.test_read_archived_figure_jun()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_aug(self):
        tested_period = 5
        self.test_read_archived_figure_jul()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_sep(self):
        tested_period = 6
        self.test_read_archived_figure_aug()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_oct(self):
        tested_period = 7
        self.test_read_archived_figure_sep()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_nov(self):
        tested_period = 8
        self.test_read_archived_figure_oct()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_dec(self):
        tested_period = 9
        self.test_read_archived_figure_nov()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_jan(self):
        tested_period = 10
        self.test_read_archived_figure_dec()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_feb(self):
        tested_period = 11
        self.test_read_archived_figure_jan()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_mar(self):
        tested_period = 12
        self.test_read_archived_figure_feb()
        self.check_archive_period(tested_period)


class EndOfMonthBudgetTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_budget()

    # The following tests test_end_of_month_xxx checkes that only forecast is saved,
    # not actuals. This is tested by counting the records saved in the period tested.
    def test_end_of_month_apr(self):
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 15)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 0)
        end_of_month_archive(1)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 30)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 1)

    def test_end_of_month_may(self):
        self.test_end_of_month_apr()
        end_of_month_archive(2)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 44)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 2)

    def test_end_of_month_jun(self):
        self.test_end_of_month_may()
        end_of_month_archive(3)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 57)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 3)

    def test_end_of_month_jul(self):
        self.test_end_of_month_jun()
        end_of_month_archive(4)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 69)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 4)

    def test_end_of_month_aug(self):
        self.test_end_of_month_jul()
        end_of_month_archive(5)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 80)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 5)

    def test_end_of_month_sep(self):
        self.test_end_of_month_aug()
        end_of_month_archive(6)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 90)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 6)

    def test_end_of_month_oct(self):
        self.test_end_of_month_sep()
        end_of_month_archive(7)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 99)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 7)

    def test_end_of_month_nov(self):
        self.test_end_of_month_oct()
        end_of_month_archive(8)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 107)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 8)

    def test_end_of_month_dec(self):
        self.test_end_of_month_nov()
        end_of_month_archive(9)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 114)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 9)

    def test_end_of_month_jan(self):
        self.test_end_of_month_dec()
        end_of_month_archive(10)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 120)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 10)

    def test_end_of_month_feb(self):
        self.test_end_of_month_jan()
        end_of_month_archive(11)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 125)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 11)

    def test_end_of_month_mar(self):
        self.test_end_of_month_feb()
        end_of_month_archive(12)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 129)
        budget_total_count = MonthlyTotalBudget.objects.all().count()
        self.assertEqual(budget_total_count, 12)


class ReadArchivedBudgetTest(TestCase, RequestFactoryBase):
    archived_figure = []

    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_budget()
        for period in range(0, 16):
            self.archived_figure.append(0)

    def get_period_total(self, period):
        data_model = forecast_budget_view_model[period]
        tot_q = data_model.objects.all()
        return tot_q[0].budget

    def get_current_total(self):
        return self.get_period_total(0)

    def check_archive_period(self, tested_period):
        total_before = self.get_current_total()
        end_of_month_archive(tested_period)
        # run a query giving the full total
        archived_total = self.get_period_total(tested_period)
        self.assertEqual(total_before, archived_total)
        change_amount = tested_period * 10000
        self.init_data.monthly_figure_update(tested_period + 1, change_amount, "budget")
        current_total = self.get_current_total()
        self.archived_figure[tested_period] = archived_total
        self.assertNotEqual(current_total, archived_total)
        self.assertNotEqual(current_total, archived_total)
        self.assertEqual(current_total, (archived_total + change_amount))

        for period in range(1, tested_period + 1):
            # Check the full total. It is saved in a different table, for convenience
            monthly_budget = MonthlyTotalBudget.objects.get(
                archived_period=period)
            self.assertEqual(
                self.archived_figure[period], monthly_budget.amount
            )
            # Check that nothig has corrupted the archived figures
            self.assertEqual(
                self.archived_figure[period], self.get_period_total(period)
            )

    # The following tests check that the archived figures are not changed by
    # changing the current figures.
    def test_read_archived_figure_apr(self):
        tested_period = 1
        self.check_archive_period(tested_period)

    def test_read_archived_figure_may(self):
        tested_period = 2
        self.test_read_archived_figure_apr()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_jun(self):
        tested_period = 3
        self.test_read_archived_figure_may()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_jul(self):
        tested_period = 4
        self.test_read_archived_figure_jun()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_aug(self):
        tested_period = 5
        self.test_read_archived_figure_jul()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_sep(self):
        tested_period = 6
        self.test_read_archived_figure_aug()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_oct(self):
        tested_period = 7
        self.test_read_archived_figure_sep()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_nov(self):
        tested_period = 8
        self.test_read_archived_figure_oct()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_dec(self):
        tested_period = 9
        self.test_read_archived_figure_nov()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_jan(self):
        tested_period = 10
        self.test_read_archived_figure_dec()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_feb(self):
        tested_period = 11
        self.test_read_archived_figure_jan()
        self.check_archive_period(tested_period)

    def test_read_archived_figure_mar(self):
        tested_period = 12
        self.test_read_archived_figure_feb()
        self.check_archive_period(tested_period)
