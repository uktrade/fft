from django.test import (
    TestCase,
)

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year, get_financial_year_obj

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


class FutureFigureSetup:
    def monthly_figure_create(self, period, amount, year_obj, what="Forecast"):
        if what == "Forecast":
            data_model = ForecastMonthlyFigure
        else:
            data_model = BudgetMonthlyFigure
        month_figure = data_model.objects.create(
            financial_period=FinancialPeriod.objects.get(financial_period_code=period),
            financial_code=self.financial_code_obj,
            financial_year=year_obj,
            amount=amount,
        )
        month_figure.save()

    def __init__(self, test_year):
        self.year_period_dict = {}
        self.year_total_budget_dict = {}

        group_name = "Test Group"
        self.group_code = "TestGG"
        directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

        group_obj = DepartmentalGroupFactory(
            group_code=self.group_code, group_name=group_name,
        )
        directorate_obj = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=directorate_name,
            group=group_obj,
        )
        cost_centre_obj = CostCentreFactory(
            directorate=directorate_obj, cost_centre_code=self.cost_centre_code,
        )
        
        programme_obj = ProgrammeCodeFactory()
        self.programme_code = programme_obj.programme_code
        nac_obj = NaturalCodeFactory(economic_budget_code="RESOURCE")
        self.nac = nac_obj.natural_account_code
        project_obj = ProjectCodeFactory()
        self.project_code = project_obj.project_code
        self.test_year = test_year
        self._test_year_obj = None
        self.current_year_obj = FinancialYear.objects.get(current=True)

        self.financial_code_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cost_centre_obj,
            natural_account_code=nac_obj,
            project_code=project_obj,
        )
        self.financial_code_obj.save


    def setup_forecast(self, future:bool):
        value_dict = {}
        if future:
            year_obj = get_financial_year_obj(self.test_year)
            factor = 100000
        else:
            year_obj = self.current_year_obj
            factor = 200000
            
        for period in range(1, 16):
            amount = period * factor
            value_dict[period] = amount
            self.monthly_figure_create(period, amount, year_obj)
        self.year_period_dict[year_obj.financial_year] = value_dict

    def setup_budget(self, future:bool):
        total_budget = 0
        if future:
            year_obj = get_financial_year_obj(self.test_year)
            factor = 100000
        else:
            year_obj = self.current_year_obj
            factor = 300000
        for period in range(1, 16):
            amount = period * factor
            total_budget += amount
            self.monthly_figure_create(period, amount, year_obj, "Budget")
        self.year_total_budget_dict[year_obj.financial_year] = total_budget

