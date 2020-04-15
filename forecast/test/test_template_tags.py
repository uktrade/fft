from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from forecast.templatetags.forecast_permissions import (
    is_forecast_user,
)


class EditPermissionTest(TestCase):
    def setUp(self):
        self.test_cost_centre = 888812

    def test_is_forecast_user(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert not is_forecast_user(test_user)

        # Give user permission to view forecasts
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        test_user.user_permissions.add(can_view_forecasts)
        test_user.save()

        # Bust permissions cache (refresh_from_db does not work)
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert is_forecast_user(test_user)
