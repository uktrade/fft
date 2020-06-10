from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.test import TestCase

from guardian.shortcuts import (
    get_objects_for_user as guardian_get_objects_for_user,
)

from costcentre.test.factories import (
    CostCentreFactory,
)

from forecast.permission_shortcuts import (
    assign_perm,
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
            accept_global_perms=False,
        )

        assert len(cost_centres) == 1

        # Check that log entry was created for assignment
        log_entry = LogEntry.objects.last()

        assert log_entry.object_id == str(self.cost_centre.cost_centre_code)
        assert log_entry.change_message == "Cost Centre permission was assigned"
