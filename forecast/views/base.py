from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse

from costcentre.models import CostCentre


class NoCostCentreCodeInURLError(Exception):
    pass


class ForecastViewPermissionMixin(UserPassesTestMixin):
    cost_centre_code = None

    def test_func(self):
        return self.request.user.has_perm(
            "forecast.can_view_forecasts"
        )

    def handle_no_permission(self):
        return redirect(
            reverse(
                "index",
            )
        )


class CostCentrePermissionTest(UserPassesTestMixin):
    cost_centre_code = None

    def test_func(self):
        if not self.request.user.has_perm("forecast.can_view_forecasts"):
            raise PermissionDenied()

        if 'cost_centre_code' not in self.kwargs:
            raise NoCostCentreCodeInURLError(
                "No cost centre code provided in URL"
            )

        self.cost_centre_code = self.kwargs["cost_centre_code"]

        cost_centre = CostCentre.objects.get(
            cost_centre_code=self.kwargs["cost_centre_code"]
        )

        return self.request.user.has_perm(
            "view_costcentre", cost_centre
        ) and self.request.user.has_perm(
            "change_costcentre",
            cost_centre
        )

    def handle_no_permission(self):
        return redirect(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    "cost_centre_code": self.cost_centre_code
                }
            )
        )
