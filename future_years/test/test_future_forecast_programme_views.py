from bs4 import BeautifulSoup


from django.urls import reverse

from forecast.test.test_utils import (
    TOTAL_COLUMN,
    SPEND_TO_DATE_COLUMN,
    UNDERSPEND_COLUMN,
    format_forecast_figure,
)

from future_years.test.future_year_utils import FutureYearForecastSetup


class ViewProgrammeDetailsTest(FutureYearForecastSetup):

    def check_programme_details_table(self, table):
        details_rows = table.find_all("tr")

        last_details_cols = details_rows[-1].find_all("td")
        # Check the total for the year
        assert last_details_cols[TOTAL_COLUMN].get_text().strip() == \
            format_forecast_figure(self.year_total)
        # Check the difference between budget and year total
        assert last_details_cols[UNDERSPEND_COLUMN].get_text().strip() == \
            format_forecast_figure(self.underspend_total)
        # Check the spend to date
        assert last_details_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
            format_forecast_figure(self.spend_to_date_total)

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

        # Check that the only table displays  the correct totals
        self.check_programme_details_table(tables[0])

    def test_view_directory_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_directorate",
                kwargs={
                    'directorate_code': self.directorate_code,
                    'programme_code': self.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_group_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_group",
                kwargs={
                    'group_code': self.group_code,
                    'programme_code': self.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                    "period": self.future_year,
                },
            ),
        )

        self.check_response(resp)

    def test_view_dit_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_dit",
                kwargs={
                    'programme_code': self.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)


class ViewProgrammeDetailsTwoYearDataTest(ViewProgrammeDetailsTest):
    def setUp(self):
        super().setUp()
        self.create_another_year()
