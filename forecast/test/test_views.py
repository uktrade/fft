from bs4 import BeautifulSoup

from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import intcomma
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

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)

from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)
from forecast.test.factories import MonthlyFigureFactory
from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
    EditForecastView,
)


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

    def add_row_get_response(self, url):
        request = self.factory.get(url)
        request.user = self.test_user
        kwargs = {
            'cost_centre_code': self.cost_centre_code
        }  # required because factory does not pass kwargs to request
        return AddRowView.as_view()(request, **kwargs)

    def add_row_post_response(self, url, post_content):
        request = self.factory.post(
            url,
            post_content,
        )
        request.user = self.test_user
        kwargs = {
            'cost_centre_code': self.cost_centre_code
        }  # required because factory does not pass kwargs to request
        return AddRowView.as_view()(request, **kwargs)

    def edit_row_get_response(self):
        edit_view_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            },
        )
        request = self.factory.get(edit_view_url)
        request.user = self.test_user
        kwargs = {
            'cost_centre_code': self.cost_centre_code
        }  # required because factory does not pass kwargs to request
        return EditForecastView.as_view()(request, **kwargs)

    def test_view_add_row(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        edit_response = self.edit_row_get_response()
        self.assertEqual(edit_response.status_code, 200)

        soup = BeautifulSoup(
            edit_response.rendered_content,
            features="html.parser",
        )
        table_rows = soup.find_all("tr", class_="govuk-table__row")

        # There should only be 2 rows (for the header and footer)
        assert len(table_rows) == 2

        add_resp = self.add_row_get_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            )
        )

        self.assertEqual(add_resp.status_code, 200)

        # add_forecast_row
        add_row_resp = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
            }
        )

        self.assertEqual(add_row_resp.status_code, 302)

        edit_response = self.edit_row_get_response()
        self.assertEqual(edit_response.status_code, 200)

        soup = BeautifulSoup(edit_response.rendered_content, features="html.parser")
        table_rows = soup.find_all("tr", class_="govuk-table__row")

        # Now we should have 3 rows (header, footer and new row)
        assert len(table_rows) == 3

    def test_duplicate_values_invalid(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        # add forecast row
        response = self.add_row_post_response(
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
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(MonthlyFigure.objects.count(), 12)

        response_2 = self.add_row_post_response(
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
            }
        )

        self.assertEqual(response_2.status_code, 200)

        assert "govuk-list govuk-error-summary__list" in str(
            response_2.rendered_content,
        )
        self.assertEqual(MonthlyFigure.objects.count(), 12)


class ChooseCostCentreTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.cost_centre_code = 109076
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        self.test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )
        self.test_user.set_password("test_password")

        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

    def factory_get(self, url):
        request = self.factory.get(url)
        request.user = self.test_user
        kwargs = {
            'cost_centre_code': self.cost_centre_code
        }  # required because factory does not pass kwargs to request
        return ChooseCostCentreView.as_view()(request, **kwargs)

    def factory_post(self, url, post_content):
        request = self.factory.post(
            url,
            post_content,
        )
        request.user = self.test_user
        kwargs = {
            'cost_centre_code': self.cost_centre_code
        }  # required because factory does not pass kwargs to request
        return ChooseCostCentreView.as_view()(request, **kwargs)

    def test_choose_cost_centre(self):
        response = self.factory_get(
            reverse(
                "choose_cost_centre"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        response = self.factory_post(
            reverse(
                "choose_cost_centre"
            ), {
                "cost_centre": self.cost_centre_code
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        # Check we've been forwarded to edit page
        assert "/forecast/edit/" in response.url


class ViewCostCentreDashboard(TestCase):
    cost_centre_code = 888812
    amount = 9876543

    def setUp(self):
        self.apr_amount = MonthlyFigureFactory.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            cost_centre=CostCentreFactory.create(
                cost_centre_code=self.cost_centre_code
            ),
            amount=self.amount,
        )

    def test_view_cost_centre_dashboard(self):
        resp = self.client.get(reverse("pivotmulti"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")

        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there are 3 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 3

        # Check that the first table displays the cost centre code
        rows = tables[0].find_all("tr")
        cols = rows[1].find_all("td")
        assert int(cols[2].get_text()) == self.cost_centre_code

        # Check the April value
        assert cols[4].get_text() == intcomma(self.amount)

        # Check the total for the year
        assert cols[-3].get_text() == intcomma(self.amount)

        # Check the difference between budget and year total
        assert cols[-2].get_text() == intcomma(-self.amount)

        # Check that all the subtotals exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 14


class ViewForecastHierarchyTest(TestCase):
    def setUp(self):
        self.group_name = "Test Group"
        self.group_code = "TestGG"

        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 888888

        self.group = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=self.group_name,
        )
        self.directorate = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=self.group,
        )
        self.cost_centre = CostCentreFactory(
            directorate=self.directorate,
            cost_centre_code=self.cost_centre_code,
        )

    def test_dit_view(self):
        response = self.client.get(
            reverse("forecast_dit")
        )

        self.assertEqual(response.status_code, 200)

        # Check group is shown
        assert self.group_name in str(response.content)

    def test_group_view(self):
        response = self.client.get(
            reverse(
                "forecast_group",
                kwargs={
                    'group_code': self.group.group_code
                },
            )
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert self.directorate_name in str(response.content)

    def test_directorate_view(self):
        response = self.client.get(
            reverse(
                "forecast_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code
                },
            )
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert str(self.cost_centre_code) in str(response.content)

    def test_cost_centre_view(self):
        response = self.client.get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre.cost_centre_code
                },
            )
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert str(self.cost_centre_code) in str(response.content)
