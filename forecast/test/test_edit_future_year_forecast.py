from bs4 import BeautifulSoup

from datetime import datetime

from django.contrib.auth.models import (
    Permission,
)
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.test.test_base import BaseTestCase
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_financial_year_obj,
)

from costcentre.test.factories import (
    CostCentreFactory,
)

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
    ForecastEditState,
    FutureForecastEditState,
)
from forecast.permission_shortcuts import assign_perm
from forecast.test.factories import FinancialCodeFactory
from forecast.test.test_edit_forecast_views import AddForecastRowTest


class AddFutureForecastRowTest(AddForecastRowTest):
    def SetUp(self):
        super().setUp()
        future_year_obj = get_financial_year_obj(self.financial_year + 1)
        self.financial_year = future_year_obj.financial_year


class EditForecastTest(BaseTestCase):
    def setUp(self):
        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")

        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()
        self.client.force_login(self.test_user)

        self.cost_centre_code = 888812
        self.current_year_amount = 12345600
        self.next_year_amount = 89765400
        self.next_next_year_amount = 1212122100

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        financial_code_obj = FinancialCode.objects.create(
            programme=ProgrammeCodeFactory.create(),
            cost_centre=self.cost_centre,
            natural_account_code=NaturalCodeFactory.create(),
        )
        financial_code_obj.save

        self.current_financial_year = get_current_financial_year()
        this_year_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(financial_period_code=1),
            financial_code=financial_code_obj,
            financial_year=get_financial_year_obj(self.current_financial_year),
            amount=self.current_year_amount,
        )
        this_year_figure.save

        next_year_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(financial_period_code=1),
            financial_code=financial_code_obj,
            financial_year=get_financial_year_obj(self.current_financial_year + 1),
            amount=self.next_year_amount,
        )
        next_year_figure.save

        next_next_year_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(financial_period_code=1),
            financial_code=financial_code_obj,
            financial_year=get_financial_year_obj(self.current_financial_year + 2),
            amount=self.next_next_year_amount,
        )
        next_next_year_figure.save

    def test_correct_current_forecast(self):
        # Checks the 'Edit-Forecast tab' returns an 'OK' status code
        edit_forecast_url = reverse(
            "edit_forecast", kwargs={"cost_centre_code": self.cost_centre_code}
        )

        response = self.client.get(edit_forecast_url)
        assert response.status_code == 200
        assert str(self.current_year_amount) in str(response.content)
        assert str(self.next_year_amount) not in str(response.content)
        assert str(self.next_next_year_amount) not in str(response.content)

    def test_correct_future_forecast(self):
        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.current_financial_year + 1,
            },
        )

        response = self.client.get(edit_forecast_url)
        assert response.status_code == 200
        assert str(self.current_year_amount) not in str(response.content)
        assert str(self.next_year_amount) in str(response.content)
        assert str(self.next_next_year_amount) not in str(response.content)

    def test_correct_next_future_forecast(self):
        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.current_financial_year + 2,
            },
        )

        response = self.client.get(edit_forecast_url)
        assert response.status_code == 200
        assert str(self.current_year_amount) not in str(response.content)
        assert str(self.next_year_amount) not in str(response.content)
        assert str(self.next_next_year_amount) in str(response.content)


class EditFutureForecastFigureViewTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        current_year = get_current_financial_year()
        future_year_obj = get_financial_year_obj(current_year + 1)
        self.future_financial_year = future_year_obj.financial_year

        self.nac_code = 999999
        self.cost_centre_code = 888812

        self.programme = ProgrammeCodeFactory.create()
        self.nac = NaturalCodeFactory.create(
            natural_account_code=self.nac_code,
        )

        self.cost_centre_code = 888812
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.financial_code = FinancialCodeFactory.create(
            programme=self.programme,
            cost_centre=self.cost_centre,
            natural_account_code=self.nac,
        )

        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

    def test_edit_forecast_(self):
        update_forecast_figure_url = reverse(
            "update_forecast_figure",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.future_financial_year,
            },
        )

        amount = 12345678
        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.future_financial_year
            ).count()
            == 0
        )
        resp = self.client.post(
            update_forecast_figure_url,
            data={
                "natural_account_code": self.nac_code,
                "programme_code": self.programme.programme_code,
                "month": 5,
                "amount": amount,
            },
        )
        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.future_financial_year
            ).count()
            == 1
        )

        self.assertEqual(resp.status_code, 200)

        assert (
            ForecastMonthlyFigure.objects.filter(
                financial_year_id=self.future_financial_year
            )
            .first()
            .amount
            == amount
        )


class EditForecastShowWarningTest(BaseTestCase):
    def setUp(self):
        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")

        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()
        self.client.force_login(self.test_user)

        self.cost_centre_code = 888812

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        self.current_financial_year = get_current_financial_year()
        self.future_year = get_current_financial_year() + 1
        get_financial_year_obj(self.future_year)

    def test_current_forecast(self):
        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.current_financial_year,
            },
        )
        response = self.client.get(edit_forecast_url)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, features="html.parser")
        divs = soup.find_all("div", class_="govuk-tag")
        assert len(divs) == 0

        divs = soup.find_all("div", class_="govuk-notification-banner__content")
        assert len(divs) == 0

    def test_future_forecast(self):
        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.future_year,
            },
        )
        response = self.client.get(edit_forecast_url)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, features="html.parser")
        divs = soup.find_all("div", class_="govuk-tag")
        assert len(divs) == 1
        divs = soup.find_all("div", class_="govuk-notification-banner__content")
        assert len(divs) == 1


class EditFutureForecastLockTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.cost_centre_code = 888812
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        self.future_year = get_current_financial_year() + 1
        get_financial_year_obj(self.future_year)

    def test_edit_forecast_view_permission(self):
        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.future_year,
            },
        )

        # Should be allowed
        resp = self.client.get(edit_forecast_url)

        self.assertEqual(resp.status_code, 200)

        # Lock forecast for editing
        edit_lock = FutureForecastEditState.objects.get()
        edit_lock.lock_date = datetime.now()
        edit_lock.save()

        # Should be redirected to lock page
        resp = self.client.get(edit_forecast_url)

        editing_locked_url = reverse("edit_unavailable")

        assert resp.status_code == 302
        assert resp.url == editing_locked_url

        # Add edit whilst lock permission
        can_edit_whilst_locked = Permission.objects.get(
            codename="can_edit_future_whilst_locked"
        )
        self.test_user.user_permissions.add(can_edit_whilst_locked)
        self.test_user.save()

        # User should not be allowed to view page
        resp = self.client.get(edit_forecast_url)

        # Should be allowed
        self.assertEqual(resp.status_code, 200)


class ChooseCostCentreFutureTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.cost_centre_code = 109076
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        self.current_year = get_current_financial_year()
        self.future_year = self.current_year + 1
        get_financial_year_obj(self.future_year)


    def test_cost_centre_json(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.client.get(reverse("choose_cost_centre"))

        self.assertEqual(
            response.status_code,
            200,
        )

        year_list = f'window.financialYears = [{{"financial_year": {self.current_year}, "financial_year_display": "Current"}}'  # noqa E501

        self.assertContains(response, year_list)

        # Lock future forecast for editing
        edit_lock = FutureForecastEditState.objects.get()
        edit_lock.lock_date = datetime.now()
        edit_lock.save()

        response = self.client.get(reverse("choose_cost_centre"))

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertNotContains(response, year_list)

    def test_cost_centre_future_json(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.client.get(reverse("choose_cost_centre"))

        self.assertEqual(
            response.status_code,
            200,
        )

        current_year_list = f'window.financialYears = [{{"financial_year": {self.current_year}, "financial_year_display": "Current"}}'  # noqa E501
        # No year selection available
        self.assertContains(response, current_year_list)

        # Lock current forecast for editing
        edit_lock = ForecastEditState.objects.get()
        edit_lock.lock_date = datetime.now()
        edit_lock.save()

        response = self.client.get(reverse("choose_cost_centre"))

        self.assertEqual(
            response.status_code,
            200,
        )
        # Current year is not on the page
        self.assertNotContains(response, current_year_list)
        future_year_list = f'window.financialYears = [{{"financial_year": {self.future_year},'  # noqa E501
        self.assertContains(response, future_year_list)

