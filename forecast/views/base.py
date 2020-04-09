from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from forecast.utils.access_helpers import (
    can_edit_cost_centre,
    can_forecast_be_edited,
    can_view_forecasts,
)


class NoCostCentreCodeInURLError(Exception):
    pass


class ForecastViewPermissionMixin(UserPassesTestMixin):
    cost_centre_code = None

    def test_func(self):
        return can_view_forecasts(self.request.user)

    def handle_no_permission(self):
        return redirect(
            reverse(
                "index",
            )
        )


class CostCentrePermissionTest(UserPassesTestMixin):
    cost_centre_code = None
    edit_not_available = False

    def test_func(self):
        if 'cost_centre_code' not in self.kwargs:
            raise NoCostCentreCodeInURLError(
                "No cost centre code provided in URL"
            )

        self.cost_centre_code = self.kwargs['cost_centre_code']

        has_permission = can_edit_cost_centre(
            self.request.user,
            self.cost_centre_code,
        )

        user_can_edit = can_forecast_be_edited(self.request.user)

        if not user_can_edit:
            self.edit_not_available = True
            return False

        return has_permission

    def handle_no_permission(self):
        if self.edit_not_available:
            return redirect(
                reverse("edit_unavailable")
            )
        else:
            return redirect(
                reverse(
                    "forecast_cost_centre",
                    kwargs={
                        "cost_centre_code": self.cost_centre_code
                    }
                )
            )
