from django.contrib.auth import get_user_model
from django.test import TestCase

from guardian.shortcuts import assign_perm

from costcentre.test.factories import (
    CostCentreFactory,
)

from forecast.templatetags.forecast_permissions import (
    has_edit_permission,
)
from forecast.views.edit_forecast import (
    TEST_COST_CENTRE,
)


class EditPermissionTest(TestCase):
    def test_has_edit_permission(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        cost_centre = CostCentreFactory.create(
            cost_centre_code=TEST_COST_CENTRE
        )

        assert not has_edit_permission(test_user)

        assign_perm("view_costcentre", test_user, cost_centre)
        assign_perm("change_costcentre", test_user, cost_centre)

        assert has_edit_permission(test_user) is True
