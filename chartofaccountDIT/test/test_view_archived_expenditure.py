from io import StringIO

from bs4 import BeautifulSoup

from django.core.management import call_command
from django.urls import reverse

from chartofaccountDIT.test.factories import ExpenditureCategoryFactory

from core.test.test_base import BaseTestCase
from core.utils.generic_helpers import get_current_financial_year


class ArchiveExpenditureCategoryTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.out = StringIO()

        obj = ExpenditureCategoryFactory()
        self.grouping_description = obj.grouping_description
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1
        call_command(
            "archive", "Expenditure_Cat", year=self.archive_year, stdout=self.out,
        )

    def test_view_historical_financecategory(self):
        response = self.client.get(
            reverse(
                "historical_finance_category",
                kwargs={"year": self.archive_year},
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1
        header_text = soup.find_all("th", class_="govuk-table__head meta-col")
        assert len(header_text) == 0
        first_cols = table_rows[0].find_all("td")
        assert first_cols[1].get_text().strip() == self.grouping_description

    def test_view_filtered_historical_financecategory(self):
        filter_parameter = "?search_all=" + self.grouping_description
        response = self.client.get(
            reverse("historical_finance_category", kwargs={"year": self.archive_year},)
            + filter_parameter,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1
        header_text = soup.find_all("th", class_="govuk-table__head meta-col")
        assert len(header_text) == 0
        first_cols = table_rows[0].find_all("td")
        assert first_cols[1].get_text().strip() == self.grouping_description
