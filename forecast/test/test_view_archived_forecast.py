from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.urls import reverse

from core.test.test_base import BaseTestCase
from end_of_month.test.test_utils import SetFullYearArchive
from forecast.test.test_utils import (
    EXPENDITURE_TABLE_INDEX,
    HIERARCHY_TABLE_INDEX,
    PROGRAMME_TABLE_INDEX,
    PROJECT_TABLE_INDEX,
    format_forecast_figure,
)


TOTAL_COLUMN = -6


class ViewArchivedForecastHierarchyTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        self.archive = SetFullYearArchive()

    def total_column_index(self, period):
        if period == 1:
            # Previous month variance is not displayed when showing April data,
            # because there is not a previous month.
            # So the total is at a different position.
            return TOTAL_COLUMN + 1
        return TOTAL_COLUMN

    def check_programme_table(self, table, prog_index, period=0):
        programme_rows = table.find_all("tr")
        first_prog_cols = programme_rows[2].find_all("td")

        self.assertEqual(
            first_prog_cols[prog_index + 2].get_text().strip(),
            format_forecast_figure(self.archive.archived_budget[period] / 100),
        )
        total_col_pos = self.total_column_index(period)

        last_programme_cols = programme_rows[-1].find_all("td")
        # Check the total for the year
        self.assertEqual(
            last_programme_cols[total_col_pos].get_text().strip(),
            format_forecast_figure(self.archive.archived_forecast[period] / 100),
        )

    def check_expenditure_table(self, table, period):
        expenditure_rows = table.find_all("tr")
        first_expenditure_cols = expenditure_rows[2].find_all("td")
        self.assertEqual(
            first_expenditure_cols[2].get_text().strip(),
            format_forecast_figure(self.archive.archived_budget[period] / 100),
        )

        last_expenditure_cols = expenditure_rows[-1].find_all("td")
        total_col_pos = self.total_column_index(period)

        # Check the total for the year
        self.assertEqual(
            last_expenditure_cols[total_col_pos].get_text().strip(),
            format_forecast_figure(self.archive.archived_forecast[period] / 100),
        )

    def check_project_table(self, table, period):
        project_rows = table.find_all("tr")
        first_project_cols = project_rows[2].find_all("td")

        self.assertEqual(
            first_project_cols[1].get_text().strip(), self.archive.project_code
        )
        self.assertEqual(
            first_project_cols[3].get_text().strip(),
            format_forecast_figure(self.archive.archived_budget[period] / 100),
        )

        last_project_cols = project_rows[-1].find_all("td")
        total_col_pos = self.total_column_index(period)

        # Check the total for the year
        self.assertEqual(
            last_project_cols[total_col_pos].get_text().strip(),
            format_forecast_figure(self.archive.archived_forecast[period] / 100),
        )

    def check_hierarchy_table(self, table, hierarchy_element, offset, period):
        hierarchy_rows = table.find_all("tr")
        first_hierarchy_cols = hierarchy_rows[2].find_all("td")
        self.assertEqual(
            first_hierarchy_cols[2 + offset].get_text().strip(), str(hierarchy_element)
        )

        budget_col = 3 + offset
        self.assertEqual(
            first_hierarchy_cols[budget_col].get_text().strip(),
            format_forecast_figure(self.archive.archived_budget[period] / 100),
        )

        last_hierarchy_cols = hierarchy_rows[-1].find_all("td")
        total_col_pos = self.total_column_index(period)

        # Check the total for the year
        self.assertEqual(
            last_hierarchy_cols[total_col_pos].get_text().strip(),
            format_forecast_figure(self.archive.archived_forecast[period] / 100),
        )

    def check_period_list(self, period_list):
        self.assertIn("Current", period_list)
        self.assertIn("April", period_list)
        self.assertIn("May", period_list)
        self.assertIn("June", period_list)
        self.assertIn("July", period_list)
        self.assertIn("August", period_list)
        self.assertIn("September", period_list)
        self.assertIn("October", period_list)
        self.assertIn("November", period_list)
        self.assertIn("December", period_list)
        self.assertIn("January", period_list)
        self.assertIn("February", period_list)
        self.assertIn("March", period_list)

    def view_cost_centre_summary(self, test_period):
        resp = self.client.get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    "cost_centre_code": self.archive.cost_centre_code,
                    "period": test_period,
                },
            ),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        self.assertContains(resp, "govuk-table")
        # Check that the month dropdown exists.
        self.assertContains(resp, f'value="{test_period}"')

        # Check that the selected period is in the view
        select_period = soup.find(id="id_selected_period")

        # Check that all the months are in the dropdown.
        self.check_period_list(str(select_period))

        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        # Check that the first table displays the cost centre code and correct values
        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.archive.cost_centre_code, 0, test_period
        )

        # Check that the second table displays the programme and the correct totals
        # The programme table in the cost centre does not show the 'View'
        # so the programme is displayed in a different column
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1, test_period)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX], test_period)

        # Check that the last table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX], test_period)

    def test_view_cost_centre_summary_apr(self):
        self.view_cost_centre_summary(1)

    def test_view_cost_centre_summary_may(self):
        self.view_cost_centre_summary(2)

    def test_view_cost_centre_summary_jun(self):
        self.view_cost_centre_summary(3)

    def test_view_cost_centre_summary_jul(self):
        self.view_cost_centre_summary(4)

    def test_view_cost_centre_summary_aug(self):
        self.view_cost_centre_summary(5)

    def test_view_cost_centre_summary_sep(self):
        self.view_cost_centre_summary(6)

    def test_view_cost_centre_summary_oct(self):
        self.view_cost_centre_summary(7)

    def test_view_cost_centre_summary_nov(self):
        self.view_cost_centre_summary(8)

    def test_view_cost_centre_summary_dec(self):
        self.view_cost_centre_summary(9)

    def test_view_cost_centre_summary_jan(self):
        self.view_cost_centre_summary(10)

    def test_view_cost_centre_summary_feb(self):
        self.view_cost_centre_summary(11)

    def test_view_cost_centre_summary_mar(self):
        self.view_cost_centre_summary(12)

    def test_view_cost_centre_summary_current(self):
        self.view_cost_centre_summary(0)

    def view_directorate_summary(self, test_period):
        resp = self.client.get(
            reverse(
                "forecast_directorate",
                kwargs={
                    "directorate_code": self.archive.directorate_code,
                    "period": test_period,
                },
            ),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that the month dropdown exists.
        self.assertContains(resp, f'value="{test_period}"')

        # Check that the selected period is in the view
        select_period = soup.find(id="id_selected_period")

        # Check that all the months are in the dropdown.
        self.check_period_list(str(select_period))

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.archive.cost_centre_code, 0, test_period
        )

        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1, test_period)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX], test_period)

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX], test_period)

    def test_view_directorate_summary_apr(self):
        self.view_directorate_summary(1)

    def test_view_directorate_summary_may(self):
        self.view_directorate_summary(2)

    def test_view_directorate_summary_jun(self):
        self.view_directorate_summary(3)

    def test_view_directorate_summary_jul(self):
        self.view_directorate_summary(4)

    def test_view_directorate_summary_aug(self):
        self.view_directorate_summary(5)

    def test_view_directorate_summary_sep(self):
        self.view_directorate_summary(6)

    def test_view_directorate_summary_oct(self):
        self.view_directorate_summary(7)

    def test_view_directorate_summary_nov(self):
        self.view_directorate_summary(8)

    def test_view_directorate_summary_dec(self):
        self.view_directorate_summary(9)

    def test_view_directorate_summary_jan(self):
        self.view_directorate_summary(10)

    def test_view_directorate_summary_feb(self):
        self.view_directorate_summary(11)

    def test_view_directorate_summary_mar(self):
        self.view_directorate_summary(12)

    def test_view_directorate_summary_current(self):
        self.view_directorate_summary(0)

    def view_group_summary(self, test_period):
        response = self.client.get(
            reverse(
                "forecast_group",
                kwargs={
                    "group_code": self.archive.group_code,
                    "period": test_period,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that the month dropdown exists.
        self.assertContains(response, f'value="{test_period}"')

        # Check that the periods is in the view
        select_period = soup.find(id="id_selected_period")

        # Check that all the months are in the dropdown.
        self.check_period_list(str(select_period))

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.archive.directorate_code, 0, test_period
        )
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1, test_period)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX], test_period)

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX], test_period)

    def test_view_group_summary_apr(self):
        self.view_group_summary(1)

    def test_view_group_summary_may(self):
        self.view_group_summary(2)

    def test_view_group_summary_jun(self):
        self.view_group_summary(3)

    def test_view_group_summary_jul(self):
        self.view_group_summary(4)

    def test_view_group_summary_aug(self):
        self.view_group_summary(5)

    def test_view_group_summary_sep(self):
        self.view_group_summary(6)

    def test_view_group_summary_oct(self):
        self.view_group_summary(7)

    def test_view_group_summary_nov(self):
        self.view_group_summary(8)

    def test_view_group_summary_dec(self):
        self.view_group_summary(9)

    def test_view_group_summary_jan(self):
        self.view_group_summary(10)

    def test_view_group_summary_feb(self):
        self.view_group_summary(11)

    def test_view_group_summary_mar(self):
        self.view_group_summary(12)

    def test_view_group_summary_current(self):
        self.view_group_summary(0)

    def view_dit_summary(self, test_period):
        response = self.client.get(
            reverse(
                "forecast_dit",
                kwargs={
                    "period": test_period,
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

        # Check that the month dropdown exists.
        self.assertContains(response, f'value="{test_period}"')

        # Check that the selected period is in the view
        select_period = soup.find(id="id_selected_period")

        # Check that all the months are in the dropdown.
        self.check_period_list(str(select_period))

        self.check_hierarchy_table(
            tables[HIERARCHY_TABLE_INDEX], self.archive.group_code, 0, test_period
        )
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1, test_period)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX], test_period)

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX], test_period)

    def test_view_dit_summary_apr(self):
        self.view_dit_summary(1)

    def test_view_dit_summary_may(self):
        self.view_dit_summary(2)

    def test_view_dit_summary_jun(self):
        self.view_dit_summary(3)

    def test_view_dit_summary_jul(self):
        self.view_dit_summary(4)

    def test_view_dit_summary_aug(self):
        self.view_dit_summary(5)

    def test_view_dit_summary_sep(self):
        self.view_dit_summary(6)

    def test_view_dit_summary_oct(self):
        self.view_dit_summary(7)

    def test_view_dit_summary_nov(self):
        self.view_dit_summary(8)

    def test_view_dit_summary_dec(self):
        self.view_dit_summary(9)

    def test_view_dit_summary_jan(self):
        self.view_dit_summary(10)

    def test_view_dit_summary_feb(self):
        self.view_dit_summary(11)

    def test_view_dit_summary_mar(self):
        self.view_dit_summary(12)

    def test_view_dit_summary_current(self):
        self.view_dit_summary(0)
