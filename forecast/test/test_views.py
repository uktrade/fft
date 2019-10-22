from bs4 import BeautifulSoup
from guardian.shortcuts import assign_perm

from django.test import (
    RequestFactory,
    TestCase,
)
from django.urls import reverse
from django.contrib.auth import (
    get_user_model,
)
from forecast.views import EditForecastView
from costcentre.test.factories import CostCentreFactory
from chartofaccountDIT.test.factories import (
    ProgrammeCodeFactory,
    NaturalCodeFactory,
)


class ViewPermissionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.cost_centre_code = 888812
        self.test_user_email = "test@test.com"
        self.test_password = "test_password"

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email
        )

        self.test_user.set_password(
            self.test_password
        )

    def test_edit_forecast_view(self):
        self.assertFalse(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

        request = self.factory.get(
            reverse('edit_forecast')
        )
        request.user = self.test_user

        resp = EditForecastView.as_view()(request)

        # Should have been redirected (no permission)
        self.assertEqual(resp.status_code, 302)

        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre
        )
        assign_perm(
            "view_costcentre",
            self.test_user,
            self.cost_centre
        )

        self.assertTrue(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )
        self.assertTrue(
            self.test_user.has_perm(
                "view_costcentre",
                self.cost_centre,
            )
        )

        request = self.factory.get(
            reverse('edit_forecast')
        )
        request.user = self.test_user

        resp = EditForecastView.as_view()(request)

        # Should be allowed
        self.assertEqual(
            resp.status_code,
            200,
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
