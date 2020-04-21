from io import StringIO

from bs4 import BeautifulSoup

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
)
from chartofaccountDIT.views import (
    HistoricalFilteredAnalysis1ListView,
    HistoricalFilteredAnalysis2ListView,
)

from core.myutils import get_current_financial_year
from core.test.test_base import RequestFactoryBase


class ArchiveAnalysis1Test(TestCase, RequestFactoryBase):
    def setUp(self):
        self.out = StringIO()
        RequestFactoryBase.__init__(self)

        self.analysis1_code = 123456
        self.analysis1_description = "Analysis1 description"
        Analysis1Factory(
            analysis1_code=self.analysis1_code,
            analysis1_description=self.analysis1_description,
        )
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1

    def show_historical_view(self):
        response = self.factory_get(
            reverse("historical_analysis_1", kwargs={"year": self.archive_year},),
            HistoricalFilteredAnalysis1ListView,
            year=self.archive_year,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        return soup

    def test_view_historical_analisys1(self):
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 2

        call_command(
            "archive", type="Analysis1", year=self.archive_year, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.analysis1_code)
        assert first_cols[1].get_text().strip() == self.analysis1_description


class ArchiveAnalysis2Test(TestCase, RequestFactoryBase):
    def setUp(self):
        self.out = StringIO()
        RequestFactoryBase.__init__(self)

        self.analysis2_code = 123456
        self.analysis2_description = "analysis2 description"
        Analysis2Factory(
            analysis2_code=self.analysis2_code,
            analysis2_description=self.analysis2_description,
        )
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1

    def show_historical_view(self):
        response = self.factory_get(
            reverse("historical_analysis_2", kwargs={"year": self.archive_year},),
            HistoricalFilteredAnalysis2ListView,
            year=self.archive_year,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        return soup

    def test_view_historical_analisys1(self):
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 2

        call_command(
            "archive", type="Analysis2", year=self.archive_year, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.analysis2_code)
        assert first_cols[1].get_text().strip() == self.analysis2_description
