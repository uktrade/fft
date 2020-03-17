from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    ExpenditureCategoryFactory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)
from core.models import FinancialYear
from core.myutils import get_current_financial_year
from core.test.test_base import RequestFactoryBase
from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)
from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastEditLock,
    ForecastMonthlyFigure,
)
from forecast.permission_shortcuts import assign_perm
from forecast.test.test_utils import create_budget
from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
    EditForecastView,
)
from forecast.test.test_views import format_forecast_figure
from forecast.views.view_forecast.project_details import (
    CostCentreProjectDetailsView,
    DITProjectDetailsView,
    DirectorateProjectDetailsView,
    GroupProjectDetailsView,
)
from forecast.views.view_forecast.forecast_summary import (
    CostCentreView,
    DITView,
    DirectorateView,
    GroupView,
)
from forecast.views.view_forecast.programme_details import (
    DITProgrammeDetailsView,
    DirectorateProgrammeDetailsView,
    GroupProgrammeDetailsView,
)

TOTAL_COLUMN = -5
SPEND_TO_DATE_COLUMN = -2
UNDERSPEND_COLUMN = -4

class ViewForecastProjectDetailsTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

        self.group = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=self.group_name,
        )
        self.directorate = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=self.group,
        )
        self.cost_centre = CostCentreFactory(
            directorate=self.directorate,
            cost_centre_code=self.cost_centre_code,
        )
        current_year = get_current_financial_year()
        self.amount1_apr = -9876543
        self.amount2_apr = 1000000

        programme_obj = ProgrammeCodeFactory()
        self.budget_type = programme_obj.budget_type_fk.budget_type_display
        expenditure_obj = ExpenditureCategoryFactory()
        self.expenditure_id = expenditure_obj.id
        self.nac1_obj = NaturalCodeFactory(natural_account_code=12345678,
                                           project_code=expenditure_obj
                                           )
        self.nac2_obj = NaturalCodeFactory(project_code=expenditure_obj)
        year_obj = FinancialYear.objects.get(financial_year=current_year)

        apr_period = FinancialPeriod.objects.get(financial_period_code=1)
        apr_period.actual_loaded = True
        apr_period.save()
        
        project_obj = ProjectCodeFactory()
        self.project_code = project_obj.project_code
        # If you use the MonthlyFigureFactory the test fails.
        # I cannot work out why, it may be due to using a random year....
        financial_code1_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code=self.nac1_obj,
            project_code=project_obj
        )
        financial_code1_obj.save
        financial_code2_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code=self.nac2_obj,
        )
        financial_code2_obj.save
        apr_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code1_obj,
            financial_year=year_obj,
            amount=self.amount1_apr,
        )
        apr_figure.save

        apr_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code2_obj,
            financial_year=year_obj,
            amount=self.amount2_apr
        )
        apr_figure.save

        self.amount_may = 1234567
        may_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=4
            ),
            financial_code=financial_code1_obj,
            financial_year=year_obj,
            amount=self.amount_may
        )
        may_figure.save

        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        self.budget = create_budget(financial_code2_obj, year_obj)
        self.year_total = self.amount1_apr + self.amount2_apr + self.amount_may
        self.underspend_total = \
            self.budget - self.amount1_apr - self.amount_may - self.amount2_apr
        self.spend_to_date_total = self.amount1_apr + self.amount2_apr

    def check_project_details_table(self, table):
        project_rows = table.find_all("tr")
        first_cols = project_rows[1].find_all("td")
        assert (first_cols[0].get_text().strip() ==
                self.nac2_obj.natural_account_code_description)

        assert first_cols[3].get_text().strip() == format_forecast_figure(
            self.budget / 100
        )

        last_cols = project_rows[-1].find_all("td")
        # Check the total for the year
        assert last_cols[TOTAL_COLUMN].get_text().strip() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_cols[UNDERSPEND_COLUMN].get_text().strip() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
            format_forecast_figure(self.spend_to_date_total / 100)

    def check_negative_value_formatted(self, soup, lenght):
        negative_values = soup.find_all("span", class_="negative")
        assert len(negative_values) == lenght

    def check_response(self, resp):
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")

        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 4

        self.check_negative_value_formatted(soup, 6)

        # Check that the only table displays the project and the correct totals
        self.check_project_details_table(tables[0])

    def test_view_cost_centre_project_details(self):
        resp = self.factory_get(
            reverse(
                "project_details_costcentre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code,
                    'project_code': self.project_code,
                },
            ),
            CostCentreProjectDetailsView,
            cost_centre_code=self.cost_centre_code,
            project_code=self.project_code,
        )
        self.check_response(resp)

    def test_view_directory_project_details(self):
        resp = self.factory_get(
            reverse(
                "expenditure_details_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code,
                    'project_code': self.project_code,
                },
            ),
            DirectorateProjectDetailsView,
            directorate_code=self.directorate.directorate_code,
            project_code=self.project_code,
        )
        self.check_response(resp)

    def test_view_group_project_details(self):
        resp = self.factory_get(
            reverse(
                "expenditure_details_group",
                kwargs={
                    'group_code': self.group.group_code,
                    'project_code': self.expenditure_id,
                },
            ),
            GroupProjectDetailsView,
            group_code=self.group.group_code,
            project_code=self.project_code,
        )

        self.check_response(resp)

    def test_view_dit_project_details(self):
        resp = self.factory_get(
            reverse(
                "project_details_dit",
                kwargs={
                    'project_code': self.project_code,
                },
            ),
            DITProjectDetailsView,
            project_code=self.project_code,
        )

        self.check_response(resp)
