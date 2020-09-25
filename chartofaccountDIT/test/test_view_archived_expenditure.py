from io import StringIO

from bs4 import BeautifulSoup

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from chartofaccountDIT.test.factories import ExpenditureCategoryFactory
from chartofaccountDIT.views import HistoricalFilteredExpenditureCategoryListView

from core.test.test_base import RequestFactoryBase
from core.utils.generic_helpers import get_current_financial_year


class ArchiveExpenditureCategoryTest(TestCase, RequestFactoryBase):
    def setUp(self):
        self.out = StringIO()
        RequestFactoryBase.__init__(self)

        obj = ExpenditureCategoryFactory()
        self.grouping_description = obj.grouping_description
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1
        call_command(
            "archive", type="Expenditure_Cat", year=self.archive_year, stdout=self.out,
        )

    def test_view_historical_financecategory(self):
        response = self.factory_get(
            reverse("historical_finance_category", kwargs={"year": self.archive_year},),
            HistoricalFilteredExpenditureCategoryListView,
            year=self.archive_year,
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
        response = self.factory_get(
            reverse("historical_finance_category", kwargs={"year": self.archive_year},)
            + filter_parameter,
            HistoricalFilteredExpenditureCategoryListView,
            year=self.archive_year,
            search_all=self.grouping_description,
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
