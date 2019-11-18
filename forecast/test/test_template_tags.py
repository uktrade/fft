from django.contrib.auth import get_user_model
from django.test import TestCase

from costcentre.test.factories import (
    CostCentreFactory,
)

from forecast.permission_shortcuts import assign_perm
from forecast.templatetags.forecast_permissions import (
    has_edit_permission,
    is_forecast_user,
)
from forecast.test.factories import ForecastPermissionFactory
from forecast.views.edit_forecast import (
    TEST_COST_CENTRE,
)


class EditPermissionTest(TestCase):
    def test_is_forecast_user(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert not is_forecast_user(test_user)

        # Give user permission to view forecasts
        ForecastPermissionFactory(
            user=test_user,
        )

        assert is_forecast_user(test_user)

    def test_has_edit_permission(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        # Give user permission to view forecasts
        ForecastPermissionFactory(
            user=test_user,
        )

        cost_centre = CostCentreFactory.create(
            cost_centre_code=TEST_COST_CENTRE
        )

        assert not has_edit_permission(test_user)

        assign_perm("view_costcentre", test_user, cost_centre)
        assign_perm("change_costcentre", test_user, cost_centre)

        assert has_edit_permission(test_user) is True
