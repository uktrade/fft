from bs4 import BeautifulSoup

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    ExpenditureCategoryFactory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import RequestFactoryBase
from core.utils.generic_helpers import get_current_financial_year

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.test.test_views import format_forecast_figure
from forecast.views.view_forecast.project_details import (
    CostCentreProjectDetailsView,
    DITProjectDetailsView,
    DirectorateProjectDetailsView,
    GroupProjectDetailsView,
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
        self.amount_apr = -9876543

        programme_obj = ProgrammeCodeFactory()
        self.budget_type = programme_obj.budget_type.budget_type_display
        expenditure_obj = ExpenditureCategoryFactory()
        self.expenditure_id = expenditure_obj.id
        self.nac_obj = NaturalCodeFactory(natural_account_code=12345678,
                                          expenditure_category=expenditure_obj,
                                          economic_budget_code='RESOURCE'
                                          )
        year_obj = FinancialYear.objects.get(financial_year=current_year)

        apr_period = FinancialPeriod.objects.get(financial_period_code=1)
        apr_period.actual_loaded = True
        apr_period.save()

        project_obj = ProjectCodeFactory(project_code=1234)
        self.project_code = project_obj.project_code
        # If you use the MonthlyFigureFactory the test fails.
        # I cannot work out why, it may be due to using a random year....
        financial_code1_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code=self.nac_obj,
            project_code=project_obj
        )
        financial_code1_obj.save
        self.expenditure_type = \
            financial_code1_obj.forecast_expenditure_type.forecast_expenditure_type_name
        apr_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code1_obj,
            financial_year=year_obj,
            amount=self.amount_apr,
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

        self.year_total = self.amount_apr + self.amount_may
        self.underspend_total = -self.amount_apr - self.amount_may
        self.spend_to_date_total = self.amount_apr

    def check_project_details_table(self, table):
        project_rows = table.find_all("tr")
        first_cols = project_rows[2].find_all("td")

        assert (first_cols[0].get_text().strip() == self.expenditure_type)
        assert first_cols[4].get_text().strip() == format_forecast_figure(
            self.amount_apr / 100
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

        # Check that  the total hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 3

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
                    'period': 0,
                },
            ),
            CostCentreProjectDetailsView,
            cost_centre_code=self.cost_centre_code,
            project_code=self.project_code,
            period=0,
        )
        self.check_response(resp)

    def test_view_directory_project_details(self):
        resp = self.factory_get(
            reverse(
                "project_details_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code,
                    'project_code': self.project_code,
                    'period': 0,
                },
            ),
            DirectorateProjectDetailsView,
            directorate_code=self.directorate.directorate_code,
            project_code=self.project_code,
            period=0,
        )
        self.check_response(resp)

    def test_view_group_project_details(self):
        resp = self.factory_get(
            reverse(
                "project_details_group",
                kwargs={
                    'group_code': self.group.group_code,
                    'project_code': self.expenditure_id,
                    'period': 0,
                },
            ),
            GroupProjectDetailsView,
            group_code=self.group.group_code,
            project_code=self.project_code,
            period=0,
        )

        self.check_response(resp)

    def test_view_dit_project_details(self):
        resp = self.factory_get(
            reverse(
                "project_details_dit",
                kwargs={
                    'project_code': self.project_code,
                    'period': 0,
                },
            ),
            DITProjectDetailsView,
            project_code=self.project_code,
            period=0,
        )

        self.check_response(resp)
