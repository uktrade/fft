from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)
from core.models import FinancialYear
from core.test.test_base import TEST_COST_CENTRE, BaseTestCase
from core.utils.generic_helpers import get_current_financial_year
from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)
from forecast.models import FinancialCode, FinancialPeriod, ForecastMonthlyFigure
from forecast.test.test_utils import (
    EXPENDITURE_TABLE_INDEX,
    HIERARCHY_TABLE_INDEX,
    PROGRAMME_TABLE_INDEX,
    PROJECT_TABLE_INDEX,
    SPEND_TO_DATE_COLUMN,
    TOTAL_COLUMN,
    UNDERSPEND_COLUMN,
    create_budget,
    format_forecast_figure,
)


class ViewForecastHierarchyTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = TEST_COST_CENTRE

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
        self.programme_obj = ProgrammeCodeFactory()
        nac_obj = NaturalCodeFactory()
        self.project_obj = ProjectCodeFactory()
        year_obj = FinancialYear.objects.get(financial_year=current_year)

        apr_period = FinancialPeriod.objects.get(financial_period_code=1)
        apr_period.actual_loaded = True
        apr_period.save()

        # If you use the MonthlyFigureFactory the test fails.
        # I cannot work out why, it may be due to using a random year....
        financial_code_obj = FinancialCode.objects.create(
            programme=self.programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code=nac_obj,
            project_code=self.project_obj,
        )
        # apr figure
        ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(financial_period_code=1),
            financial_code=financial_code_obj,
            financial_year=year_obj,
            amount=self.amount_apr,
        )
        self.amount_may = 1234567
        # may figure
        ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=2,
            ),
            amount=self.amount_may,
            financial_code=financial_code_obj,
            financial_year=year_obj,
        )
        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        self.budget = create_budget(financial_code_obj, year_obj)
        self.year_total = self.amount_apr + self.amount_may
        self.underspend_total = self.budget - self.amount_apr - self.amount_may
        self.spend_to_date_total = self.amount_apr

    def test_dit_view(self):
        response = self.client.get(
            reverse(
                "forecast_dit",
                kwargs={
                    "period": 0,
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        # Check group is shown
        assert self.group_name in str(response.rendered_content)

    def test_group_view(self):
        response = self.client.get(
            reverse(
                "forecast_group",
                kwargs={
                    "group_code": self.group.group_code,
                    "period": 0,
                },
            ),
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert self.directorate_name in str(response.rendered_content)

    def test_directorate_view(self):
        response = self.client.get(
            reverse(
                "forecast_directorate",
                kwargs={
                    "directorate_code": self.directorate.directorate_code,
                    "period": 0,
                },
            ),
        )
        self.assertEqual(response.status_code, 200)

        # Check cost centre is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def test_cost_centre_view(self):
        response = self.client.get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "period": 0,
                },
            ),
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def check_programme_table(self, table, prog_index=1):
        programme_rows = table.find_all("tr")
        first_prog_cols = programme_rows[2].find_all("td")
        assert (
            first_prog_cols[prog_index].get_text().strip()
            == self.programme_obj.programme_description
        )
        assert (
            first_prog_cols[prog_index + 1].get_text().strip()
            == self.programme_obj.programme_code
        )

        last_programme_cols = programme_rows[-1].find_all("td")
        # Check the total for the year
        assert last_programme_cols[
            TOTAL_COLUMN
        ].get_text().strip() == format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_programme_cols[
            UNDERSPEND_COLUMN
        ].get_text().strip() == format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_programme_cols[
            SPEND_TO_DATE_COLUMN
        ].get_text().strip() == format_forecast_figure(self.spend_to_date_total / 100)

    def check_expenditure_table(self, table):
        expenditure_rows = table.find_all("tr")
        first_expenditure_cols = expenditure_rows[2].find_all("td")
        assert first_expenditure_cols[1].get_text().strip() == "—"
        assert first_expenditure_cols[2].get_text().strip() == format_forecast_figure(
            self.budget / 100
        )

        last_expenditure_cols = expenditure_rows[-1].find_all("td")
        # Check the total for the year
        assert last_expenditure_cols[
            TOTAL_COLUMN
        ].get_text().strip() == format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_expenditure_cols[
            UNDERSPEND_COLUMN
        ].get_text().strip() == format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_expenditure_cols[
            SPEND_TO_DATE_COLUMN
        ].get_text().strip() == format_forecast_figure(self.spend_to_date_total / 100)

    def check_project_table(self, table):
        project_rows = table.find_all("tr")
        first_project_cols = project_rows[2].find_all("td")

        assert (
            first_project_cols[0].get_text().strip()
            == self.project_obj.project_description
        )
        assert first_project_cols[1].get_text().strip() == self.project_obj.project_code
        assert first_project_cols[3].get_text().strip() == format_forecast_figure(
            self.budget / 100
        )

        last_project_cols = project_rows[-1].find_all("td")
        # Check the total for the year
        assert last_project_cols[
            TOTAL_COLUMN
        ].get_text().strip() == format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_project_cols[
            UNDERSPEND_COLUMN
        ].get_text().strip() == format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_project_cols[
            SPEND_TO_DATE_COLUMN
        ].get_text().strip() == format_forecast_figure(self.spend_to_date_total / 100)

    def check_hierarchy_table(self, table, hierarchy_element, offset):
        hierarchy_rows = table.find_all("tr")
        first_hierarchy_cols = hierarchy_rows[2].find_all("td")
        assert first_hierarchy_cols[1 + offset].get_text().strip() == hierarchy_element
        budget_col = 3 + offset
        assert first_hierarchy_cols[
            budget_col
        ].get_text().strip() == format_forecast_figure(self.budget / 100)
        assert first_hierarchy_cols[
            budget_col + 1
        ].get_text().strip() == format_forecast_figure(self.amount_apr / 100)

        last_hierarchy_cols = hierarchy_rows[-1].find_all("td")
        # Check the total for the year
        assert last_hierarchy_cols[
            TOTAL_COLUMN
        ].get_text().strip() == format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_hierarchy_cols[
            UNDERSPEND_COLUMN
        ].get_text().strip() == format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_hierarchy_cols[
            SPEND_TO_DATE_COLUMN
        ].get_text().strip() == format_forecast_figure(self.spend_to_date_total / 100)

    def check_negative_value_formatted(self, soup):
        negative_values = soup.find_all("span", class_="negative")
        assert len(negative_values) == 42

    def test_view_cost_centre_summary(self):
        resp = self.client.get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "period": 0,
                },
            ),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")
        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4
        # Check the existence of header showing Actual/Forecast labels
        header_text = soup.find_all("th", class_="govuk-table__head meta-col")
        assert len(header_text) != 0

        # Check that the first table displays the cost centre code
        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_negative_value_formatted(soup)

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.cost_centre.cost_centre_name, 0
        )

        # Check that the second table displays the programme and the correct totals
        # The programme table in the cost centre does not show the 'View'
        # so the programme is displayed in a different column
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_directorate_summary(self):
        resp = self.client.get(
            reverse(
                "forecast_directorate",
                kwargs={
                    "directorate_code": self.directorate.directorate_code,
                    "period": 0,
                },
            ),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_negative_value_formatted(soup)

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.cost_centre.cost_centre_name, 0
        )

        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_group_summary(self):
        response = self.client.get(
            reverse(
                "forecast_group",
                kwargs={
                    "group_code": self.group.group_code,
                    "period": 0,
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_negative_value_formatted(soup)

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.directorate.directorate_name, 0
        )
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_dit_summary(self):
        response = self.client.get(
            reverse(
                "forecast_dit",
                kwargs={
                    "period": 0,
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierarchy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_negative_value_formatted(soup)

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX], self.group_name, 0)
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])
