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
)
from forecast.permission_shortcuts import assign_perm


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
            "edit_forecast", kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.current_financial_year + 1,
            }
        )

        response = self.client.get(edit_forecast_url)
        assert response.status_code == 200
        assert str(self.current_year_amount) not in str(response.content)
        assert str(self.next_year_amount) in str(response.content)
        assert str(self.next_next_year_amount) not in str(response.content)

    def test_correct_next_future_forecast(self):
        edit_forecast_url = reverse(
            "edit_forecast", kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.current_financial_year + 2,
            }
        )

        response = self.client.get(edit_forecast_url)
        assert response.status_code == 200
        assert str(self.current_year_amount) not in str(response.content)
        assert str(self.next_year_amount) not in str(response.content)
        assert str(self.next_next_year_amount) in str(response.content)
