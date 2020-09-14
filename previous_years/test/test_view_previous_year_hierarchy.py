from bs4 import BeautifulSoup


from django.urls import reverse

from forecast.test.test_utils import (
    format_forecast_figure,
)
from forecast.views.view_forecast.forecast_summary import (
    CostCentreView,
    DITView,
    DirectorateView,
    GroupView,
)

from previous_years.test.test_utils import (
    DownloadPastYearForecastSetup,
    hide_adjustment_columns
)

TOTAL_COLUMN = -5
SPEND_TO_DATE_COLUMN = -2
UNDERSPEND_COLUMN = -4

HIERARCHY_TABLE_INDEX = 0
PROGRAMME_TABLE_INDEX = 1
EXPENDITURE_TABLE_INDEX = 2
PROJECT_TABLE_INDEX = 3


class ViewForecastHierarchyTest(DownloadPastYearForecastSetup):
    def test_dit_view(self):
        response = self.factory_get(
            reverse(
                "forecast_dit",
                kwargs={
                    "period": self.archived_year,
                },
            ),
            DITView,
            period=self.archived_year,
        )

        self.assertEqual(response.status_code, 200)

        # Check group is shown
        assert self.group_name in str(response.rendered_content)

    def test_group_view(self):
        response = self.factory_get(
            reverse(
                "forecast_group",
                kwargs={
                    'group_code': self.group_code,
                    "period": self.archived_year,
                },
            ),
            GroupView,
            group_code=self.group_code,
            period=self.archived_year,
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert self.directorate_name in str(response.rendered_content)

    def test_directorate_view(self):
        response = self.factory_get(
            reverse(
                "forecast_directorate",
                kwargs={
                    'directorate_code': self.directorate_code,
                    "period": self.archived_year,
                },
            ),
            DirectorateView,
            directorate_code=self.directorate_code,
            period=self.archived_year,
        )
        self.assertEqual(response.status_code, 200)

        # Check cost centre is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def test_cost_centre_view(self):
        response = self.factory_get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code,
                    "period": self.archived_year,
                },
            ),
            CostCentreView,
            cost_centre_code=self.cost_centre_code,
            period=self.archived_year,
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def check_programme_table(self, table, prog_index=1):
        programme_rows = table.find_all("tr")
        first_prog_cols = programme_rows[2].find_all("td")
        assert first_prog_cols[prog_index].get_text().strip() == \
            self.programme_description
        assert first_prog_cols[prog_index + 1].get_text().strip() == \
            self.programme_code

        last_programme_cols = programme_rows[-1].find_all("td")
        # Check the total for the year
        assert last_programme_cols[TOTAL_COLUMN].get_text().strip() == \
            format_forecast_figure(self.year_total)
        # Check the difference between budget and year total
        assert last_programme_cols[UNDERSPEND_COLUMN].get_text().strip() == \
            format_forecast_figure(self.underspend_total)
        # Check the spend to date
        assert last_programme_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
            format_forecast_figure(self.spend_to_date_total)

    def check_expenditure_table(self, table):
        expenditure_rows = table.find_all("tr")
        first_expenditure_cols = expenditure_rows[2].find_all("td")
        assert first_expenditure_cols[2].get_text().strip() == format_forecast_figure(
            self.budget
        )

        last_expenditure_cols = expenditure_rows[-1].find_all("td")
        # Check the total for the year
        assert last_expenditure_cols[TOTAL_COLUMN].get_text().strip() == \
            format_forecast_figure(self.year_total)
        # Check the difference between budget and year total
        assert last_expenditure_cols[UNDERSPEND_COLUMN].get_text().strip() == \
            format_forecast_figure(self.underspend_total)
        # Check the spend to date
        assert last_expenditure_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
            format_forecast_figure(self.spend_to_date_total)

    def check_project_table(self, table):
        project_rows = table.find_all("tr")
        first_project_cols = project_rows[2].find_all("td")

        assert first_project_cols[0].get_text().strip() == \
            self.project_description
        assert first_project_cols[1].get_text().strip() == self.project_code
        assert first_project_cols[3].get_text().strip() == format_forecast_figure(
            self.budget
        )

        last_project_cols = project_rows[-1].find_all("td")
        # Check the total for the year
        assert last_project_cols[TOTAL_COLUMN].get_text().strip() == \
            format_forecast_figure(self.year_total)
        # Check the difference between budget and year total
        assert last_project_cols[UNDERSPEND_COLUMN].get_text().strip() == \
            format_forecast_figure(self.underspend_total)
        # Check the spend to date
        assert last_project_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
            format_forecast_figure(self.spend_to_date_total)

    def check_hierarchy_table(self, table, hierarchy_element, offset):
        hierarchy_rows = table.find_all("tr")
        first_hierarchy_cols = hierarchy_rows[2].find_all("td")
        assert first_hierarchy_cols[1 + offset].get_text().strip() == \
            hierarchy_element
        budget_col = 3 + offset
        assert first_hierarchy_cols[budget_col].get_text().strip() == \
            format_forecast_figure(self.budget)
        assert first_hierarchy_cols[budget_col + 1].get_text().strip() == \
            format_forecast_figure(self.outturn["apr"])

        last_hierarchy_cols = hierarchy_rows[-1].find_all("td")
        # Check the total for the year
        assert last_hierarchy_cols[TOTAL_COLUMN].get_text().strip() == \
            format_forecast_figure(self.year_total)
        # Check the difference between budget and year total
        assert last_hierarchy_cols[UNDERSPEND_COLUMN].get_text().strip() == \
            format_forecast_figure(self.underspend_total)
        # Check the spend to date
        assert last_hierarchy_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
            format_forecast_figure(self.spend_to_date_total)

    def check_negative_value_formatted(self, soup):
        negative_values = soup.find_all("span", class_="negative")
        assert len(negative_values) == 42

    def test_view_cost_centre_summary(self):
        resp = self.factory_get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code,
                    "period": self.archived_year,
                },
            ),
            CostCentreView,
            cost_centre_code=self.cost_centre_code,
            period=self.archived_year,
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

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
                                   self.cost_centre_name, 0)

        # Check that the second table displays the programme and the correct totals
        # The programme table in the cost centre does not show the 'View'
        # so the programme is displayed in a different column
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_directorate_summary(self):
        resp = self.factory_get(
            reverse(
                "forecast_directorate",
                kwargs={
                    'directorate_code': self.directorate_code,
                    "period": self.archived_year,
                },
            ),
            DirectorateView,
            directorate_code=self.directorate_code,
            period=self.archived_year,
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

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
                                   self.cost_centre_name, 0)

        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_group_summary(self):
        response = self.factory_get(
            reverse(
                "forecast_group",
                kwargs={
                    'group_code': self.group_code,
                    "period": self.archived_year,
                },
            ),
            GroupView,
            group_code=self.group_code,
            period=self.archived_year,
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

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
                                   self.directorate_name, 0)
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_dit_summary(self):
        response = self.factory_get(
            reverse(
                "forecast_dit",
                kwargs={
                    "period": self.archived_year,
                },
            ),
            DITView,
            period=self.archived_year,
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

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
                                   self.group_name, 0)
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])


class ViewForecastHierarchyAdjustmentColumnsTest(ViewForecastHierarchyTest):
    def setUp(self):
        super().setUp()
        hide_adjustment_columns()
