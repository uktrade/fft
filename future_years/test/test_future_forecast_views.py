from bs4 import BeautifulSoup

from django.contrib.auth.models import (
    Permission,
)
from django.urls import reverse

from core.utils.generic_helpers import (
    get_current_financial_year,
)

from end_of_month.test.test_utils import MonthlyFigureSetup

from core.test.test_base import BaseTestCase
from forecast.test.test_utils import (
    HIERARCHY_TABLE_INDEX,
    PROGRAMME_TABLE_INDEX,
    EXPENDITURE_TABLE_INDEX,
    PROJECT_TABLE_INDEX,
    TOTAL_COLUMN,
    format_forecast_figure,
)


class ViewFutureForecastHierarchyTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()
        self.test_year = get_current_financial_year() + 1
        # Create the figure for the year in the future
        self.forecast_data = MonthlyFigureSetup(self.test_year)
        self.forecast_data.setup_forecast()
        self.forecast_data.setup_budget()

    def check_programme_table(self, table, prog_index):
        programme_rows = table.find_all("tr")
        first_prog_cols = programme_rows[2].find_all("td")

        self.assertEqual(
            first_prog_cols[prog_index + 2].get_text().strip(),
            format_forecast_figure(self.forecast_data.total_budget / 100),
        )

        last_programme_cols = programme_rows[-1].find_all("td")
        # Check the total for the year
        self.assertEqual(
            last_programme_cols[TOTAL_COLUMN].get_text().strip(),
            format_forecast_figure(self.forecast_data.total_forecast / 100),
        )

    def check_expenditure_table(self, table):
        expenditure_rows = table.find_all("tr")
        first_expenditure_cols = expenditure_rows[2].find_all("td")
        self.assertEqual(
            first_expenditure_cols[2].get_text().strip(),
            format_forecast_figure(self.forecast_data.total_budget / 100),
        )

        last_expenditure_cols = expenditure_rows[-1].find_all("td")

        # Check the total for the year
        self.assertEqual(
            last_expenditure_cols[TOTAL_COLUMN].get_text().strip(),
            format_forecast_figure(self.forecast_data.total_forecast / 100),
        )

    def check_project_table(self, table):
        project_rows = table.find_all("tr")
        first_project_cols = project_rows[2].find_all("td")

        self.assertEqual(
            first_project_cols[1].get_text().strip(), self.forecast_data.project_code
        )
        self.assertEqual(
            first_project_cols[3].get_text().strip(),
            format_forecast_figure(self.forecast_data.total_budget / 100),
        )

        last_project_cols = project_rows[-1].find_all("td")

        # Check the total for the year
        self.assertEqual(
            last_project_cols[TOTAL_COLUMN].get_text().strip(),
            format_forecast_figure(self.forecast_data.total_forecast / 100),
        )

    def check_hierarchy_table(self, table, hierarchy_element, offset):
        hierarchy_rows = table.find_all("tr")
        first_hierarchy_cols = hierarchy_rows[2].find_all("td")
        self.assertEqual(
            first_hierarchy_cols[2 + offset].get_text().strip(), str(hierarchy_element)
        )

        budget_col = 3 + offset
        self.assertEqual(
            first_hierarchy_cols[budget_col].get_text().strip(),
            format_forecast_figure(self.forecast_data.total_budget / 100),
        )

        last_hierarchy_cols = hierarchy_rows[-1].find_all("td")

        # Check the total for the year
        self.assertEqual(
            last_hierarchy_cols[TOTAL_COLUMN].get_text().strip(),
            format_forecast_figure(self.forecast_data.total_forecast / 100),
        )

    def test_view_cost_centre_summary(self):
        resp = self.client.get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    "cost_centre_code": self.forecast_data.cost_centre_code,
                    "period": self.test_year,
                },
            ),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        self.assertContains(resp, "govuk-table")

        # Check that the year dropdown exists.
        self.assertContains(resp, f'value="{self.test_year}"')

        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        # Check that the first table displays the cost centre code and correct values
        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.forecast_data.cost_centre_code, 0
        )

        # Check that the second table displays the programme and the correct totals
        # The programme table in the cost centre does not show the 'View'
        # so the programme is displayed in a different column
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the last table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_directorate_summary(self):
        resp = self.client.get(
            reverse(
                "forecast_directorate",
                kwargs={
                    "directorate_code": self.forecast_data.directorate_code,
                    "period": self.test_year,
                },
            ),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that the month dropdown exists.
        self.assertContains(resp, f'value="{self.test_year}"')

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.forecast_data.cost_centre_code, 0
        )

        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_group_summary(self):
        response = self.client.get(
            reverse(
                "forecast_group",
                kwargs={
                    "group_code": self.forecast_data.group_code,
                    "period": self.test_year,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that the month dropdown exists.
        self.assertContains(response, f'value="{self.test_year}"')

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.forecast_data.directorate_code, 0
        )
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_dit_summary(self):
        response = self.client.get(
            reverse(
                "forecast_dit",
                kwargs={
                    "period": self.test_year,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that all the subtotal hierarchy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        # Check that the month/year dropdown exists.
        self.assertContains(response, f'value="{self.test_year}"')

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.forecast_data.group_code, 0
        )
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])
        #
        # # Check that the fourth table displays the project and the correct totals
        # self.check_project_table(tables[PROJECT_TABLE_INDEX])


class ViewFutureForecastHierarchyWithOtherDataTest(ViewFutureForecastHierarchyTest):
    # Identical to the previous test, but with more than one year data in the db
    def setUp(self):
        super().setUp()
        self.test_year = self.test_year + 1
        self.forecast_data.set_year(self.test_year)
        self.forecast_data.setup_forecast()
        self.forecast_data.setup_budget()
