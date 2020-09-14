from io import StringIO

from bs4 import BeautifulSoup

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    ProgrammeCodeFactory,
)
from chartofaccountDIT.views import (
    HistoricalFilteredProgrammeView,
)

from core.test.test_base import RequestFactoryBase
from core.utils.generic_helpers import get_current_financial_year


class ArchiveProgrammeCodeTest(TestCase, RequestFactoryBase):
    def setUp(self):
        self.out = StringIO()
        RequestFactoryBase.__init__(self)

        obj = ProgrammeCodeFactory()
        self.programme_code = obj.programme_code
        self.programme_description = obj.programme_description
        self.budget_type = obj.budget_type.budget_type
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1
        call_command(
            "archive", type="Programmes", year=self.archive_year, stdout=self.out,
        )

    def test_view_historical_programme(self):
        response = self.factory_get(
            reverse("historical_programme_filter", kwargs={"year": self.archive_year},),
            HistoricalFilteredProgrammeView,
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

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.programme_code)
        assert first_cols[1].get_text().strip() == self.programme_description
        assert first_cols[2].get_text().strip() == self.budget_type
