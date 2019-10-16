from bs4 import BeautifulSoup

from django.test import TestCase
from django.urls import reverse

from costcentre.test.factories import CostCentreFactory
from chartofaccountDIT.test.factories import (
    ProgrammeCodeFactory,
    NaturalCodeFactory,
)


class AddForecastRowTest(TestCase):
    def test_view_add_row(self):
        # Set up test objects
        programme = ProgrammeCodeFactory.create()
        nac = NaturalCodeFactory.create(
            natural_account_code=999999
        )
        CostCentreFactory.create(
            cost_centre_code=888812
        )

        edit_resp = self.client.get(
            reverse('edit_forecast')
        )
        self.assertEqual(
            edit_resp.status_code,
            200,
        )

        self.assertContains(edit_resp, "govuk-table")
        soup = BeautifulSoup(edit_resp.content, features="html.parser")
        table_rows = soup.find_all("tr", class_="govuk-table__row")

        # There should only be 2 rows (for the header and footer)
        assert len(table_rows) == 2

        add_resp = self.client.get(
            reverse('add_forecast_row')
        )
        self.assertEqual(
            add_resp.status_code,
            200,
        )

        # add_forecast_row
        add_row_resp = self.client.post(
            reverse('add_forecast_row'), {
                "programme": programme.programme_code,
                "natural_account_code": nac.natural_account_code,
            },
            follow=True,
        )

        self.assertEqual(
            add_row_resp.status_code,
            200,
        )

        self.assertContains(add_row_resp, "govuk-table")
        soup = BeautifulSoup(add_row_resp.content, features="html.parser")
        table_rows = soup.find_all("tr", class_="govuk-table__row")

        # Now we should have 3 rows (header, footer and new row)
        assert len(table_rows) == 3
