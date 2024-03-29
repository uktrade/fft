from bs4 import BeautifulSoup
from django.urls import reverse

from forecast.test.test_utils import (
    SPEND_TO_DATE_COLUMN,
    TOTAL_COLUMN,
    UNDERSPEND_COLUMN,
    format_forecast_figure,
)
from previous_years.test.test_utils import (
    PastYearForecastSetup,
    hide_adjustment_columns,
)


class ViewProjectDetailsTest(PastYearForecastSetup):
    def check_project_details_table(self, table):
        details_rows = table.find_all("tr")

        last_details_cols = details_rows[-1].find_all("td")
        # Check the total for the year
        assert last_details_cols[
            TOTAL_COLUMN
        ].get_text().strip() == format_forecast_figure(self.year_total)
        # Check the difference between budget and year total
        assert last_details_cols[
            UNDERSPEND_COLUMN
        ].get_text().strip() == format_forecast_figure(self.underspend_total)
        # Check the spend to date
        assert last_details_cols[
            SPEND_TO_DATE_COLUMN
        ].get_text().strip() == format_forecast_figure(self.spend_to_date_total)

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
        assert len(table_rows) == 3
        self.check_negative_value_formatted(soup, 6)

        # Check that the only table displays  the correct totals
        self.check_project_details_table(tables[0])

    def test_view_cost_Centre_project_details(self):
        resp = self.client.get(
            reverse(
                "project_details_costcentre",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "project_code": self.project_code,
                    "period": self.archived_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_directory_project_details(self):
        resp = self.client.get(
            reverse(
                "project_details_directorate",
                kwargs={
                    "directorate_code": self.directorate_code,
                    "project_code": self.project_code,
                    "period": self.archived_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_group_project_details(self):
        resp = self.client.get(
            reverse(
                "project_details_group",
                kwargs={
                    "group_code": self.group_code,
                    "project_code": self.project_code,
                    "period": self.archived_year,
                },
            ),
        )

        self.check_response(resp)

    def test_view_dit_project_details(self):
        resp = self.client.get(
            reverse(
                "project_details_dit",
                kwargs={
                    "project_code": self.project_code,
                    "period": self.archived_year,
                },
            ),
        )
        self.check_response(resp)


class ViewProjectDetailsAdjustmentColumnsTest(ViewProjectDetailsTest):
    def setUp(self):
        super().setUp()
        hide_adjustment_columns()


class ViewProjectDetailsTwoYearDataTest(ViewProjectDetailsTest):
    def setUp(self):
        super().setUp()
        self.create_another_year()
