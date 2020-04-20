from bs4 import BeautifulSoup

from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from core.myutils import get_current_financial_year
from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)

from costcentre.views import HistoricalFilteredCostListView


class ArchiveCostCentreTest(TestCase, RequestFactoryBase):
    def setUp(self):
        self.out = StringIO()
        RequestFactoryBase.__init__(self)

        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

        group = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=self.group_name,
        )
        directorate = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=group,
        )
        cost_centre = CostCentreFactory(
            directorate=directorate,
            cost_centre_code=self.cost_centre_code,
        )
        current_year = get_current_financial_year()
        self.archive_year = current_year-1

    def show_historical_view(self):
        response = self.factory_get(
            reverse(
                "historical_cost_centre_filter",
                kwargs={
                    'year': self.archive_year
                },
            ),
            HistoricalFilteredCostListView,
            year=self.archive_year,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        return soup

    def test_view_historical_costcentre(self):
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 2

        call_command(
            "archive",
            type='CostCentre',
            year=self.archive_year,
            stdout=self.out,
        )
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert (first_cols[0].get_text().strip() == self.group_code)
        assert (first_cols[1].get_text().strip() == self.group_name)
        assert (first_cols[2].get_text().strip() == self.directorate_code)
        assert (first_cols[3].get_text().strip() == self.directorate_name)
        assert (first_cols[4].get_text().strip() == str(self.cost_centre_code))



