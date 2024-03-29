from django.test import TestCase

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)
from core.test.test_base import TEST_COST_CENTRE
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_financial_year_obj,
)
from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)
from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.models import EndOfMonthStatus, forecast_budget_view_model
from end_of_month.utils import (
    InvalidPeriodError,
    LaterPeriodAlreadyArchivedError,
    PeriodAlreadyArchivedError,
    get_archivable_month,
    validate_period_code,
)
from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)


class MonthlyFigureSetup:
    def monthly_figure_update(self, period, amount, what="Forecast"):
        if what == "Forecast":
            data_model = ForecastMonthlyFigure
        else:
            data_model = BudgetMonthlyFigure
        month_figure = data_model.objects.get(
            financial_period=FinancialPeriod.objects.get(financial_period_code=period),
            financial_code=self.financial_code_obj,
            financial_year=self.year_obj,
            archived_status=None,
        )
        month_figure.amount += amount
        month_figure.save()

    def monthly_figure_create(self, period, amount, what="Forecast"):
        if what == "Forecast":
            data_model = ForecastMonthlyFigure
        else:
            data_model = BudgetMonthlyFigure
        month_figure = data_model.objects.create(
            financial_period=FinancialPeriod.objects.get(financial_period_code=period),
            financial_code=self.financial_code_obj,
            financial_year=self.year_obj,
            amount=amount,
        )
        month_figure.save()

    def __init__(self, year=0):
        group_name = "Test Group"
        self.group_code = "TestGG"
        directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = TEST_COST_CENTRE

        group_obj = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=group_name,
        )
        directorate_obj = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=directorate_name,
            group=group_obj,
        )
        cost_centre_obj = CostCentreFactory(
            directorate=directorate_obj,
            cost_centre_code=self.cost_centre_code,
        )
        programme_obj = ProgrammeCodeFactory()
        self.programme_code = programme_obj.programme_code
        nac_obj = NaturalCodeFactory(economic_budget_code="RESOURCE")
        self.nac = nac_obj.natural_account_code
        project_obj = ProjectCodeFactory()
        self.project_code = project_obj.project_code

        self.financial_code_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cost_centre_obj,
            natural_account_code=nac_obj,
            project_code=project_obj,
        )

        if year == 0:
            year = get_current_financial_year()

        self.set_year(year)

    def set_year(self, year):
        self.year_used = year
        self.year_obj = get_financial_year_obj(self.year_used)
        # Create different amount for different years
        self.factor = 100000 * (self.year_used - get_current_financial_year() + 1)

    def setup_forecast(self):
        self.value_dict = {}
        self.total_forecast = 0
        for period in range(1, 16):
            amount = period * self.factor
            self.total_forecast += amount
            self.value_dict[period] = amount
            self.monthly_figure_create(period, amount)

    def setup_budget(self):
        self.total_budget = 0
        for period in range(1, 16):
            amount = period * self.factor / 2
            self.total_budget += amount
            self.monthly_figure_create(period, amount, "Budget")


class SetFullYearArchive(MonthlyFigureSetup):
    def set_period_total(self, period):
        data_model = forecast_budget_view_model[period]
        tot_q = data_model.objects.all()
        self.archived_forecast[period] = (
            tot_q[0].apr
            + tot_q[0].may
            + tot_q[0].jun
            + tot_q[0].jul
            + tot_q[0].aug
            + tot_q[0].sep
            + tot_q[0].oct
            + tot_q[0].nov
            + tot_q[0].dec
            + tot_q[0].jan
            + tot_q[0].feb
            + tot_q[0].mar
            + tot_q[0].adj1
            + tot_q[0].adj2
            + tot_q[0].adj3
        )
        self.archived_budget[period] = tot_q[0].budget

    def set_archive_period(self, last_archived_period=13):
        if last_archived_period > 13:
            last_archived_period = 13
        for tested_period in range(1, last_archived_period):
            end_of_month_archive(tested_period)
            # save the full total
            self.set_period_total(tested_period)
            change_amount = tested_period * 10000
            self.monthly_figure_update(tested_period + 1, change_amount, "Forecast")
            change_amount = tested_period * 1000
            self.monthly_figure_update(tested_period + 1, change_amount, "Budget")
        self.set_period_total(0)

    def __init__(self, last_archived_period=16, year=0):
        super().__init__(year)
        self.archived_forecast = []
        self.archived_budget = []
        self.setup_forecast()
        self.setup_budget()
        # prepares the lists used to store the totals
        for _ in range(0, last_archived_period):
            self.archived_forecast.append(0)
            self.archived_budget.append(0)
        self.set_archive_period(last_archived_period)


class UtilsTests(TestCase):
    def test_validate_period_code(self):
        with self.assertRaises(InvalidPeriodError):
            validate_period_code(period_code=0)
        with self.assertRaises(InvalidPeriodError):
            validate_period_code(period_code=16)

        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=4
        )
        end_of_month_info.archived = True
        end_of_month_info.save()

        with self.assertRaises(PeriodAlreadyArchivedError):
            validate_period_code(period_code=4)

        with self.assertRaises(LaterPeriodAlreadyArchivedError):
            validate_period_code(period_code=2)

    def test_get_archivable_month(self):
        obj = FinancialPeriod.objects.get(pk=2)
        obj.actual_loaded = True
        obj.save()
        last_month_with_actual = FinancialPeriod.financial_period_info.actual_month()
        end_of_month_status = EndOfMonthStatus.objects.filter(
            archived_period__financial_period_code=last_month_with_actual,
        ).first()
        end_of_month_status.archived = True
        end_of_month_status.save()

        with self.assertRaises(PeriodAlreadyArchivedError):
            get_archivable_month()
