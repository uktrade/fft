from bs4 import BeautifulSoup

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from guardian.shortcuts import assign_perm

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from costcentre.test.factories import CostCentreFactory

from forecast.models import MonthlyFigure
from forecast.views.forecast_views import EditForecastView


# Nb. we're using RequestFactory here
# because SSO does not fully support
# the test client's user object
class ViewPermissionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.cost_centre_code = 109076
        self.test_user_email = "test@test.com"
        self.test_password = "test_password"

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email
        )

        self.test_user.set_password(self.test_password)

    def test_edit_forecast_view(self):
        self.assertFalse(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre
            )
        )

        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

        request = self.factory.get(edit_forecast_url)
        request.user = self.test_user
        kwargs = {
            'cost_centre_code': self.cost_centre_code
        }  # required because factory does not pass kwargs to request

        resp = EditForecastView.as_view()(request, **kwargs)

        # Should have been redirected (no permission)
        self.assertEqual(resp.status_code, 302)

        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        self.assertTrue(self.test_user.has_perm("change_costcentre", self.cost_centre))
        self.assertTrue(self.test_user.has_perm("view_costcentre", self.cost_centre))

        request = self.factory.get(edit_forecast_url)
        request.user = self.test_user

        resp = EditForecastView.as_view()(request, **kwargs)

        # Should be allowed
        self.assertEqual(resp.status_code, 200)


class AddForecastRowTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.nac_code = 999999
        self.cost_centre_code = 888812
        self.analysis_1_code = "1111111"
        self.analysis_2_code = "2222222"
        self.project_code = "3000"

        self.programme = ProgrammeCodeFactory.create()
        self.nac = NaturalCodeFactory.create(natural_account_code=self.nac_code)
        self.project = ProjectCodeFactory.create(project_code=self.project_code)
        self.analysis_1 = Analysis1Factory.create(analysis1_code=self.analysis_1_code)
        self.analysis_2 = Analysis2Factory.create(analysis2_code=self.analysis_2_code)
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.test_user_email = "test@test.com"
        self.test_password = "test_password"

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email
        )

        self.test_user.set_password(self.test_password)

    def test_view_add_row(self):
        # Set up test objects
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

        request = self.factory.get(edit_forecast_url)
        request.user = self.test_user
        kwargs = {
            'cost_centre_code': self.cost_centre_code
        }  # required because factory does not pass kwargs to request
        edit_resp = EditForecastView.as_view()(request, **kwargs)

        self.assertEqual(edit_resp.status_code, 200)

        self.assertContains(edit_resp, "govuk-table")
        soup = BeautifulSoup(edit_resp.content, features="html.parser")
        table_rows = soup.find_all("tr", class_="govuk-table__row")

        # There should only be 2 rows (for the header and footer)
        assert len(table_rows) == 2

        add_resp = self.client.get(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            )
        )
        self.assertEqual(add_resp.status_code, 200)

        # add_forecast_row
        add_row_resp = self.client.post(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
            },
            follow=True,
        )

        self.assertEqual(add_row_resp.status_code, 200)

        self.assertContains(add_row_resp, "govuk-table")
        soup = BeautifulSoup(add_row_resp.content, features="html.parser")
        table_rows = soup.find_all("tr", class_="govuk-table__row")

        # Now we should have 3 rows (header, footer and new row)
        assert len(table_rows) == 3

    def test_duplicate_values_invalid(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        # add_forecast_row
        response = self.client.post(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(MonthlyFigure.objects.count(), 12)

        response_2 = self.client.post(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
            follow=True,
        )

        self.assertEqual(response_2.status_code, 200)

        assert "govuk-list govuk-error-summary__list" in str(
            response_2.content,
        )
        self.assertEqual(MonthlyFigure.objects.count(), 12)


class ChooseCostCentreTest(TestCase):
    def setUp(self):
        self.cost_centre_code = 109076
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_view_choose_cost_centre(self):
        resp = self.client.get(
            reverse(
                "choose_cost_centre"
            )
        )

        self.assertEqual(
            resp.status_code,
            200,
        )

        resp = self.client.post(
            reverse(
                "choose_cost_centre"
            ), {
                "cost_centre": self.cost_centre_code
            },
            follow=True,
        )

        self.assertEqual(
            resp.status_code,
            200,
        )

        # If the post has worked, we will have been
        # redirect twice, first to the edit page and
        # then to the cost centre page (because we don't
        # have permission to view the edit page)
        self.assertEqual(
            len(resp.redirect_chain),
            2
        )
        assert resp.redirect_chain[0] == (
            '/forecast/edit/{}/'.format(
                self.cost_centre_code,
            ),
            302,
        )
        assert resp.redirect_chain[1] == (
            '/forecast/costcentre/',
            302,
        )


class ViewCostCentreDashboard(TestCase):
    def setUp(self):
        self.programme = ProgrammeCodeFactory.create()
        self.nac = NaturalCodeFactory.create(natural_account_code=999999)

        self.cost_centre_code = 109076

    def testView(self):
        pass
