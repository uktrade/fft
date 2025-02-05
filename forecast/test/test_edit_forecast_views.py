from datetime import datetime

from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)
from core.test.test_base import TEST_COST_CENTRE, BaseTestCase
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_financial_year_obj,
)
from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)
from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastEditState,
    ForecastMonthlyFigure,
)
from forecast.permission_shortcuts import assign_perm
from forecast.test.factories import FinancialCodeFactory


class AddForecastRowTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.nac_code = 999999
        self.cost_centre_code = TEST_COST_CENTRE
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
        self.financial_year = get_current_financial_year()

    def add_row_get_response(self, url):
        return self.client.get(url)

    def add_row_post_response(self, url, post_content):
        return self.client.post(
            url,
            data=post_content,
        )

    def edit_row_get_response(self):
        edit_view_url = reverse(
            "edit_forecast",
            kwargs={"cost_centre_code": self.cost_centre_code},
        )

        return self.client.get(edit_view_url)

    def test_view_add_row(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        assert FinancialCode.objects.count() == 0

        add_resp = self.add_row_get_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "financial_year": self.financial_year,
                },
            ),
        )
        self.assertEqual(add_resp.status_code, 200)

        add_row_resp = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "financial_year": self.financial_year,
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
            },
        )

        self.assertEqual(add_row_resp.status_code, 302)

        assert FinancialCode.objects.count() == 1

    def test_view_add_row_with_period_actual(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        # financial period with actual
        financial_period = FinancialPeriod.objects.get(
            financial_period_code=1,
        )
        financial_period.actual_loaded = True
        financial_period.save()

        assert ForecastMonthlyFigure.objects.count() == 0

        add_row_resp = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "financial_year": self.financial_year,
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
            },
        )

        self.assertEqual(add_row_resp.status_code, 302)

        assert ForecastMonthlyFigure.objects.count() == 1

        monthly_figure = ForecastMonthlyFigure.objects.first()

        assert (
            monthly_figure.financial_period.financial_period_code
            == financial_period.financial_period_code
        )  # noqa

    def test_duplicate_values_invalid(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "financial_year": self.financial_year,
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(FinancialCode.objects.count(), 1)

        response_2 = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "financial_year": self.financial_year,
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
        )

        self.assertEqual(response_2.status_code, 200)

        assert "govuk-list govuk-error-summary__list" in str(
            response_2.rendered_content,
        )
        self.assertEqual(FinancialCode.objects.count(), 1)

    def test_duplicate_values_different_cost_centre_valid(self):
        cost_centre_code_2 = self.cost_centre_code + 1

        cost_centre_2 = CostCentreFactory.create(
            cost_centre_code=cost_centre_code_2,
        )

        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("change_costcentre", self.test_user, cost_centre_2)

        # add forecast row
        response = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "financial_year": self.financial_year,
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(FinancialCode.objects.count(), 1)

        response_2 = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    "cost_centre_code": cost_centre_code_2,
                    "financial_year": self.financial_year,
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
        )

        self.assertEqual(response_2.status_code, 302)
        self.assertEqual(FinancialCode.objects.count(), 2)


class AddFutureForecastRowTest(AddForecastRowTest):
    def setUp(self):
        super().setUp()
        future_year_obj = get_financial_year_obj(self.financial_year + 1)
        self.financial_year = future_year_obj.financial_year


class ChooseCostCentreTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.cost_centre_code = TEST_COST_CENTRE
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_choose_cost_centre(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.client.get(reverse("choose_cost_centre"))

        self.assertEqual(
            response.status_code,
            200,
        )

        response = self.client.post(
            reverse("choose_cost_centre"),
            data={"cost_centre": self.cost_centre_code},
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        # Check we've been forwarded to edit page
        assert "/forecast/edit/" in response.url

    def test_cost_centre_json(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.client.get(reverse("choose_cost_centre"))

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            f'window.costCentres = [{{"name": "{self.cost_centre.cost_centre_name}", "code": "{self.cost_centre_code}"}}];',  # noqa E501
        )

    def test_finance_admin_cost_centre_access(self):
        finance_admins = Group.objects.get(
            name="Finance Administrator",
        )
        finance_admins.user_set.add(self.test_user)
        finance_admins.save()

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user.email
        )

        # Check that the cost centres can be accessed
        response = self.client.get(reverse("choose_cost_centre"))

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_finance_business_partner_cost_centre_access(self):
        finance_business_partners = Group.objects.get(
            name="Finance Business Partner/BSCE",
        )
        finance_business_partners.user_set.add(self.test_user)
        finance_business_partners.save()

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user.email
        )

        # Check that no cost centres can be accessed
        response = self.client.get(reverse("choose_cost_centre"))
        assert response.status_code == 403

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.client.get(
            reverse("choose_cost_centre"),
        )

        self.assertEqual(
            response.status_code,
            200,
        )


class EditCostCentre000Test(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.cost_centre_code = "000001"
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_choose_cost_centre(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        edit_forecast_url = reverse(
            "edit_forecast", kwargs={"cost_centre_code": self.cost_centre_code}
        )

        # Should be allowed
        resp = self.client.get(edit_forecast_url)

        self.assertEqual(resp.status_code, 200)


class EditForecastLockTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.cost_centre_code = TEST_COST_CENTRE
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_edit_forecast_view_permission(self):
        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        edit_forecast_url = reverse(
            "edit_forecast", kwargs={"cost_centre_code": self.cost_centre_code}
        )

        # Should be allowed
        resp = self.client.get(edit_forecast_url)

        self.assertEqual(resp.status_code, 200)

        # Lock forecast for editing
        edit_lock = ForecastEditState.objects.get()
        edit_lock.lock_date = datetime.now()
        edit_lock.save()

        # Should be redirected to lock page
        resp = self.client.get(edit_forecast_url)

        editing_locked_url = reverse(
            "edit_unavailable",
            kwargs={
                "financial_year": get_current_financial_year(),
            },
        )

        assert resp.status_code == 302
        assert resp.url == editing_locked_url

        # Add edit whilst lock permission
        can_edit_whilst_locked = Permission.objects.get(
            codename="can_edit_whilst_locked"
        )
        self.test_user.user_permissions.add(can_edit_whilst_locked)
        self.test_user.save()

        # User should not be allowed to view page
        resp = self.client.get(edit_forecast_url)

        # Should be allowed
        self.assertEqual(resp.status_code, 200)


class EditForecastFigureViewTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.financial_year = get_current_financial_year()
        self.nac_code = 999999
        self.cost_centre_code = TEST_COST_CENTRE

        self.programme = ProgrammeCodeFactory.create()
        self.nac = NaturalCodeFactory.create(
            natural_account_code=self.nac_code,
        )

        self.cost_centre_code = TEST_COST_CENTRE
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        FinancialCodeFactory.create(
            programme=self.programme,
            cost_centre=self.cost_centre,
            natural_account_code=self.nac,
        )

        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

    def test_edit_forecast_max_amount(self):
        update_forecast_figure_url = reverse(
            "update_forecast_figure",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.financial_year,
            },
        )

        amount = 999999999999999999
        assert amount > settings.MAX_FORECAST_FIGURE

        resp = self.client.post(
            update_forecast_figure_url,
            data={
                "natural_account_code": self.nac_code,
                "programme_code": self.programme.programme_code,
                "month": 5,
                "amount": amount,
            },
        )

        self.assertEqual(resp.status_code, 200)

        assert (
            ForecastMonthlyFigure.objects.first().amount == settings.MAX_FORECAST_FIGURE
        )  # noqa

    def test_edit_forecast_min_amount(self):
        update_forecast_figure_url = reverse(
            "update_forecast_figure",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.financial_year,
            },
        )

        amount = -999999999999999999
        assert amount < settings.MIN_FORECAST_FIGURE

        resp = self.client.post(
            update_forecast_figure_url,
            data={
                "natural_account_code": self.nac_code,
                "programme_code": self.programme.programme_code,
                "month": 5,
                "amount": amount,
            },
        )

        self.assertEqual(resp.status_code, 200)

        assert (
            ForecastMonthlyFigure.objects.first().amount == settings.MIN_FORECAST_FIGURE
        )  # noqa


class ViewEditTest(BaseTestCase):
    def setUp(self):
        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")

        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        self.client.force_login(self.test_user)

        self.group = DepartmentalGroupFactory()

        self.directorate = DirectorateFactory(
            group=self.group,
        )
        self.financial_year = get_current_financial_year()
        self.test_cost_centre = TEST_COST_CENTRE
        self.cost_centre_code = self.test_cost_centre
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

    def test_edit_to_view_cost_centre_code(self):
        # Checks the 'Edit-Forecast tab' returns an 'OK' status code
        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.financial_year,
            },
        )

        response = self.client.get(edit_forecast_url)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        # Checks CC href in the 'Edit Forecast' tab links to 'View Forecast' CC tab
        view_forecast_url = reverse(
            "forecast_cost_centre",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "period": self.financial_year,
            },
        )

        response = self.client.get(view_forecast_url)
        assert response.status_code == 200

        cost_centre_links = soup.find_all("a", class_="cost-centre-heading-link")

        assert len(cost_centre_links) == 1
        assert cost_centre_links[0]["href"] == view_forecast_url

        # Checks Group Code in 'Edit Forecast' tab links to 'View Forecast' GC tab
        view_group_forecast_url = reverse(
            "forecast_group",
            kwargs={
                "group_code": self.group.group_code,
                "period": self.financial_year,
            },
        )

        group_code_links = soup.find_all("a", class_="group-link")

        assert len(group_code_links) == 1
        assert group_code_links[0]["href"] == view_group_forecast_url

        # Checks Directorate in 'Edit Forecast' tab links to 'View Forecast' tab
        view_directorate_forecast_url = reverse(
            "forecast_directorate",
            kwargs={
                "directorate_code": self.directorate.directorate_code,
                "period": self.financial_year,
            },
        )

        directorate_code_links = soup.find_all("a", class_="directorate-link")

        assert len(directorate_code_links) == 1
        assert directorate_code_links[0]["href"] == view_directorate_forecast_url
