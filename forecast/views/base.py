from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from costcentre.models import CostCentre

from forecast.models import ForecastEditLock
from forecast.permission_shortcuts import (
    NoForecastViewPermission,
    get_objects_for_user,
)


class NoCostCentreCodeInURLError(Exception):
    pass


def can_edit_forecast(user):
    # Check for edit being locked
    forecast_edit_lock = ForecastEditLock.objects.get()

    if (
        forecast_edit_lock.locked and
        not user.has_perm(
            "forecast.can_edit_whilst_locked",
        )
    ):
        return False

    return True


def has_edit_permission(user, cost_centre_code):
    if not user.has_perm("forecast.can_view_forecasts"):
        return False

    cost_centre = CostCentre.objects.get(
        cost_centre_code=cost_centre_code,
    )

    if not user.has_perm(
        "change_costcentre",
        cost_centre
    ):
        return False

    try:
        cost_centres = get_objects_for_user(
            user,
            "costcentre.change_costcentre",
        )
    except NoForecastViewPermission:
        return False

    # If user has permission on
    # one or more CCs then let them view
    return cost_centres.count() > 0


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
    edit_locked = False

    def test_func(self):
        if 'cost_centre_code' not in self.kwargs:
            raise NoCostCentreCodeInURLError(
                "No cost centre code provided in URL"
            )

        self.cost_centre_code = self.kwargs['cost_centre_code']

        has_permission = has_edit_permission(
            self.request.user,
            self.cost_centre_code,
        )

        can_edit = can_edit_forecast(self.request.user)

        if not can_edit:
            self.edit_locked = True
            return False

        return has_permission

    def handle_no_permission(self):
        if self.edit_locked:
            return redirect(
                reverse("edit_locked")
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
