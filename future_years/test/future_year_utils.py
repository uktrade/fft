from core.test.test_base import BaseTestCase

from django.contrib.auth.models import Permission

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
    ExpenditureCategoryFactory,
)

from core.models import FinancialYear
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_financial_year_obj,
)

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
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

    def setup_forecast(self, future: bool):
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

    def setup_budget(self, future: bool):
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



class FutureYearForecastSetup(BaseTestCase):

    def set_year(self, year):
        self.future_year = year
        self.future_year_obj = get_financial_year_obj(year)
        # Create different results for different years
        self.factor = 100000 * (year - get_current_financial_year() + 1)

    def setUp(self):
        self.client.force_login(self.test_user)
        self.set_year(get_current_financial_year() + 1)
        self.cost_centre_code = "109189"
        self.cost_centre_name = "Test cost centre"
        self.group_code = "1090TT"
        self.group_name = "Test group name"
        self.directorate_code = "10900T"
        self.directorate_name = "Test directorate name"
        self.natural_account_code = 52191003
        self.natural_account_description = "Test nac description"
        self.programme_code = "310940"
        self.programme_description = "Test programme description"
        self.project_code = "0123"
        self.project_description = "Test project description"
        self.analisys1 = "00798"
        self.analisys2 = "00321"
        group_obj = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=self.group_name,
        )
        directorate_obj = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=group_obj,
        )

        cc_obj = CostCentreFactory.create(
            directorate=directorate_obj,
            cost_centre_code=self.cost_centre_code,
            cost_centre_name=self.cost_centre_name,
        )

        project_obj = ProjectCodeFactory.create(
            project_code=self.project_code,
            project_description=self.project_description,
        )
        self.budget_type_id = "AME"
        programme_obj = ProgrammeCodeFactory.create(
            programme_code=self.programme_code,
            programme_description=self.programme_description,
            budget_type_id=self.budget_type_id,
        )

        expenditure_category_obj = ExpenditureCategoryFactory.create(
        )

        self.expenditure_category_id = expenditure_category_obj.id
        nac_obj = NaturalCodeFactory.create(
            natural_account_code=self.natural_account_code,
            natural_account_code_description=self.natural_account_description,
            economic_budget_code="CAPITAL",
            expenditure_category=expenditure_category_obj,
        )

        analysis2_obj = Analysis2Factory.create(
            analysis2_code=self.analisys2
        )
        analysis1_obj = Analysis1Factory.create(
            analysis1_code=self.analisys1
        )
        self.financial_code_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cc_obj,
            natural_account_code=nac_obj,
            analysis1_code=analysis1_obj,
            analysis2_code=analysis2_obj,
            project_code=project_obj,
        )

        self.expenditure_type_name = self.financial_code_obj.forecast_expenditure_type
        self.forecast_expenditure_type_id = (
            self.financial_code_obj.forecast_expenditure_type.forecast_expenditure_type_name
        )

        self.setup_forecast()
        self.setup_budget()

        self.underspend_total = self.total_budget - self.year_total
        self.spend_to_date_total = 0

        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

    def monthly_figure_create(self, period, amount, what="Forecast"):
        if what == "Forecast":
            data_model = ForecastMonthlyFigure
        else:
            data_model = BudgetMonthlyFigure
        month_figure = data_model.objects.create(
            financial_period=FinancialPeriod.objects.get(financial_period_code=period),
            financial_code=self.financial_code_obj,
            financial_year=self.future_year_obj,
            amount=amount,
        )
        month_figure.save()

    def setup_forecast(self):
        self.value_dict = {}
        self.year_total = 0
        for period in range(1, 13):
            amount = period * self.factor
            self.year_total += amount
            self.value_dict[period] = amount
            self.monthly_figure_create(period, amount)

    def setup_budget(self):
        self.total_budget = 0
        for period in range(1, 13):
            amount = period * self.factor / 2
            self.total_budget += amount
            self.monthly_figure_create(period, amount, "Budget")



