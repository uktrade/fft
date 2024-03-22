import pytest
from django.db.models import F

from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.models import forecast_budget_view_model
from end_of_month.test.test_utils import MonthlyFigureSetup


class TestReadMonthlyVarianceTest:
    @pytest.fixture(autouse=True)
    def _setup(self, db):
        self.archived_figure = [0 for _ in range(16)]
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()

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

    def get_previous_outturn(self, period):
        data_model = forecast_budget_view_model[period]
        tot_q = data_model.objects.all()
        return tot_q[0].previous_outturn

    def get_current_previous_outturn(self):
        return self.get_previous_outturn(0)

    def check_archive_period(self, tested_period):
        total_before = self.get_current_total()
        end_of_month_archive(tested_period, True)
        # run a query giving the full total
        archived_total = self.get_period_total(tested_period)
        assert total_before == archived_total

        previous_outurn = self.get_current_previous_outturn()
        assert total_before == previous_outurn

        change_amount = tested_period * 10000
        self.init_data.monthly_figure_update(tested_period + 1, change_amount)
        current_total = self.get_current_total()
        self.archived_figure[tested_period] = archived_total
        assert current_total != previous_outurn
        assert current_total == (previous_outurn + change_amount)

    # The following tests check that the previous outturn figure is not changed by
    # changing the current figures.
    def test_read_previous_outturn_apr(self):
        tested_period = 1
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_may(self):
        tested_period = 2
        self.test_read_previous_outturn_apr()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_jun(self):
        tested_period = 3
        self.test_read_previous_outturn_may()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_jul(self):
        tested_period = 4
        self.test_read_previous_outturn_jun()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_aug(self):
        tested_period = 5
        self.test_read_previous_outturn_jul()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_sep(self):
        tested_period = 6
        self.test_read_previous_outturn_aug()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_oct(self):
        tested_period = 7
        self.test_read_previous_outturn_sep()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_nov(self):
        tested_period = 8
        self.test_read_previous_outturn_oct()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_dec(self):
        tested_period = 9
        self.test_read_previous_outturn_nov()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_jan(self):
        tested_period = 10
        self.test_read_previous_outturn_dec()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_feb(self):
        tested_period = 11
        self.test_read_previous_outturn_jan()
        self.check_archive_period(tested_period)

    def test_read_previous_outturn_mar(self):
        tested_period = 12
        self.test_read_previous_outturn_feb()
        self.check_archive_period(tested_period)
