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


class ViewForecastNaturalAccountCodeTest(PastYearForecastSetup):
    def check_nac_table(self, table):
        nac_rows = table.find_all("tr")
        first_nac_cols = nac_rows[2].find_all("td")
        assert first_nac_cols[0].get_text().strip() == self.natural_account_description

        assert first_nac_cols[2].get_text().strip() == format_forecast_figure(
            self.budget
        )

        last_nac_cols = nac_rows[-1].find_all("td")
        # Check the total for the year
        assert last_nac_cols[TOTAL_COLUMN].get_text().strip() == format_forecast_figure(
            self.year_total
        )
        # Check the difference between budget and year total
        assert last_nac_cols[
            UNDERSPEND_COLUMN
        ].get_text().strip() == format_forecast_figure(self.underspend_total)
        # Check the spend to date
        assert last_nac_cols[
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

        # Check that the only table displays the nac and the correct totals
        self.check_nac_table(tables[0])

    def test_view_cost_centre_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_cost_centre",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "expenditure_category": self.expenditure_category_id,
                    "budget_type": self.budget_type_id,
                    "period": self.archived_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_directory_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_directorate",
                kwargs={
                    "directorate_code": self.directorate_code,
                    "expenditure_category": self.expenditure_category_id,
                    "budget_type": self.budget_type_id,
                    "period": self.archived_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_group_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_group",
                kwargs={
                    "group_code": self.group_code,
                    "expenditure_category": self.expenditure_category_id,
                    "budget_type": self.budget_type_id,
                    "period": self.archived_year,
                },
            ),
        )

        self.check_response(resp)

    def test_view_dit_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_dit",
                kwargs={
                    "expenditure_category": self.expenditure_category_id,
                    "budget_type": self.budget_type_id,
                    "period": self.archived_year,
                },
            ),
        )

        self.check_response(resp)


class ViewForecastNaturalAccountCodeAdjustmentColumnsTest(
    ViewForecastNaturalAccountCodeTest
):
    def setUp(self):
        super().setUp()
        hide_adjustment_columns()


class ViewForecastNaturalAccountCodeTwoYearDataTest(ViewForecastNaturalAccountCodeTest):
    def setUp(self):
        super().setUp()
        self.create_another_year()
