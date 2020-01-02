from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from guardian.shortcuts import (
    assign_perm as guardian_assign_perm,
    get_objects_for_user as guardian_get_objects_for_user,
)

from costcentre.test.factories import (
    CostCentreFactory,
)

from forecast.permission_shortcuts import (
    NoForecastViewPermission,
    assign_perm,
    get_objects_for_user,
)


class PermissionShortcutsTest(
    TestCase,
):
    def setUp(self):
        test_cost_centre = 888812

        self.test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=test_cost_centre
        )

    def test_assign_perm(self):
        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert self.test_user.has_perm("forecast.can_view_forecasts")

        # check guardian permissions created
        cost_centres = guardian_get_objects_for_user(
            self.test_user,
            "costcentre.change_costcentre",
        )

        assert len(cost_centres) == 1

    def test_get_objects_for_user(self):
        with self.assertRaises(NoForecastViewPermission):
            get_objects_for_user(
                self.test_user,
                "costcentre.change_costcentre",
            )

        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        guardian_assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

        cost_centres = get_objects_for_user(
            self.test_user,
            "costcentre.change_costcentre",
        )

        assert len(cost_centres) == 1
