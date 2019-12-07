from bs4 import BeautifulSoup

from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)

from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)
from forecast.permission_shortcuts import assign_perm
from forecast.test.factories import (
    ForecastPermissionFactory,
    MonthlyFigureFactory,
)
from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
    EditForecastView,
)
from forecast.views.view_forecast_summary import (
    CostCentreView,
    DITView,
    DirectorateView,
    GroupView,
)


class ViewPermissionsTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.test_cost_centre = 888812
        self.cost_centre_code = self.test_cost_centre
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_edit_forecast_view_permission(self):
        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

        # Should 403 as they do not have permission
        with self.assertRaises(PermissionDenied):
            self.factory_get(
                edit_forecast_url,
                EditForecastView,
                cost_centre_code=self.cost_centre_code,
            )

    def test_edit_forecast_view(self):
        # Add forecast view permission
        ForecastPermissionFactory(
            user=self.test_user,
        )

        self.assertFalse(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

        resp = self.factory_get(
            edit_forecast_url,
            EditForecastView,
            cost_centre_code=self.cost_centre_code,
        )

        # Should have been redirected (no permission)
        self.assertEqual(resp.status_code, 302)

        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        self.assertTrue(self.test_user.has_perm("change_costcentre", self.cost_centre))
        self.assertTrue(self.test_user.has_perm("view_costcentre", self.cost_centre))

        resp = self.factory_get(
            edit_forecast_url,
            EditForecastView,
            cost_centre_code=self.cost_centre_code,
        )

        # Should be allowed
        self.assertEqual(resp.status_code, 200)


class AddForecastRowTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

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

    def add_row_get_response(self, url):
        return self.factory_get(
            url,
            AddRowView,
            cost_centre_code=self.cost_centre_code,
        )

    def add_row_post_response(self, url, post_content):
        return self.factory_post(
            url,
            post_content,
            AddRowView,
            cost_centre_code=self.cost_centre_code,
        )

    def edit_row_get_response(self):
        edit_view_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            },
        )

        return self.factory_get(
            edit_view_url,
            EditForecastView,
            cost_centre_code=self.cost_centre_code,
        )

    # TODO reinstate with edit tests
    # def test_view_add_row(self):
    #     assign_perm("change_costcentre", self.test_user, self.cost_centre)
    #     assign_perm("view_costcentre", self.test_user, self.cost_centre)
    #
    #     edit_response = self.edit_row_get_response()
    #     self.assertEqual(edit_response.status_code, 200)
    #
    #     soup = BeautifulSoup(
    #         edit_response.rendered_content,
    #         features="html.parser",
    #     )
    #     table_rows = soup.find_all("tr", class_="govuk-table__row")
    #
    #     # There should only be 2 rows (for the header and footer)
    #     assert len(table_rows) == 2
    #
    #     add_resp = self.add_row_get_response(
    #         reverse(
    #             "add_forecast_row",
    #             kwargs={
    #                 'cost_centre_code': self.cost_centre_code
    #             },
    #         )
    #     )
    #
    #     self.assertEqual(add_resp.status_code, 200)
    #
    #     # add_forecast_row
    #     add_row_resp = self.add_row_post_response(
    #         reverse(
    #             "add_forecast_row",
    #             kwargs={
    #                 'cost_centre_code': self.cost_centre_code
    #             },
    #         ),
    #         {
    #             "programme": self.programme.programme_code,
    #             "natural_account_code": self.nac.natural_account_code,
    #         }
    #     )
    #
    #     self.assertEqual(add_row_resp.status_code, 302)
    #
    #     edit_response = self.edit_row_get_response()
    #     self.assertEqual(edit_response.status_code, 200)
    #
    #     soup = BeautifulSoup(edit_response.rendered_content, features="html.parser")
    #     table_rows = soup.find_all("tr", class_="govuk-table__row")
    #
    #     # Now we should have 3 rows (header, footer and new row)
    #     assert len(table_rows) == 3

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


class ChooseCostCentreTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.cost_centre_code = 109076
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

    def test_choose_cost_centre(self):
        response = self.factory_get(
            reverse(
                "choose_cost_centre"
            ),
            ChooseCostCentreView,
            kwargs={
                'cost_centre_code': self.cost_centre_code
            },  # required because factory does not pass kwargs to request
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
            ChooseCostCentreView,
            kwargs={
                'cost_centre_code': self.cost_centre_code
            },  # required because factory does not pass kwargs to request
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        # Check we've been forwarded to edit page
        assert "/forecast/edit/" in response.url


class ViewForecastHierarchyTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

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
        self.amount_apr = 9876543
        programme_obj = ProgrammeCodeFactory()
        nac_obj = NaturalCodeFactory()

        MonthlyFigureFactory.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            programme = programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code = nac_obj,
            amount=self.amount_apr,
        )
        self.amount_may = 1234567
        MonthlyFigureFactory.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=2
            ),
            cost_centre=self.cost_centre,
            programme = programme_obj,
            natural_account_code = nac_obj,
            amount=self.amount_may,
        )

        # Assign forecast view permission
        ForecastPermissionFactory(
            user=self.test_user,
        )

    def test_dit_view(self):
        response = self.factory_get(
            reverse("forecast_dit"),
            DITView,
        )

        self.assertEqual(response.status_code, 200)

        # Check group is shown
        assert self.group_name in str(response.rendered_content)

    def test_group_view(self):
        response = self.factory_get(
            reverse(
                "forecast_group",
                kwargs={
                    'group_code': self.group.group_code
                },
            ),
            GroupView,
            group_code=self.group.group_code,
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert self.directorate_name in str(response.rendered_content)

    def test_directorate_view(self):
        response = self.factory_get(
            reverse(
                "forecast_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code
                },
            ),
            DirectorateView,
            directorate_code=self.directorate.directorate_code,
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def test_cost_centre_view(self):
        response = self.factory_get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            CostCentreView,
            cost_centre_code=self.cost_centre.cost_centre_code,
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def test_view_cost_centre_summary(self):

        q = MonthlyFigure.pivot.pivot_data()
        print(q)
        print(q.query)

        resp = self.factory_get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            CostCentreView,
            cost_centre_code=self.cost_centre_code,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code
        rows = tables[0].find_all("tr")
        cols = rows[1].find_all("td")
        assert int(cols[2].get_text()) == self.cost_centre_code

        # Check the April value
        assert cols[4].get_text() == intcomma(self.amount_apr)

        # Check the total for the year
        assert cols[-3].get_text() == intcomma(self.amount_apr)

        # Check the difference between budget and year total
        assert cols[-2].get_text() == intcomma(-self.amount_apr)

        # Check that all the subtotals exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18
