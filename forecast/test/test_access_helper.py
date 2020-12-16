from datetime import (
    datetime,
    timedelta,
)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from core.test.test_base import BaseTestCase

from costcentre.test.factories import (
    CostCentreFactory,
)

from forecast.models import (
    ForecastEditState,
)
from forecast.permission_shortcuts import assign_perm
from forecast.test.factories import UnlockedForecastEditorFactory
from forecast.utils.access_helpers import (
    can_edit_at_least_one_cost_centre,
    can_edit_cost_centre,
    can_forecast_be_edited,
    can_view_forecasts,
    is_system_closed,
    is_system_locked,
    user_in_group,
)


User = get_user_model()


class PermissionTestBase(TestCase):
    def setUp(self):
        self.cost_centre_code = 888332
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.forecast_edit_state = ForecastEditState.objects.get()

    """Assigns test user given permission and busts permission cache"""
    def assign_permission(self, codename):
        perm = Permission.objects.get(
            codename=codename,
        )
        self.test_user.user_permissions.add(perm)
        self.test_user.save()

        # Needed to bust permission cache
        self.test_user = User.objects.get(
            email=self.test_user.email
        )


class TestSimpleAccessHelpers(BaseTestCase, PermissionTestBase):
    def setUp(self):
        super().setUp()

    def test_can_view_forecasts_forecast_view_perm(self):
        assert not can_view_forecasts(self.test_user)

        self.assign_permission("can_view_forecasts")

        assert can_view_forecasts(self.test_user)

    def test_can_view_forecasts_cost_centre_perm(self):
        assert not can_view_forecasts(self.test_user)

        # Add cost centre edit permission
        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

        assert can_view_forecasts(self.test_user)

    def test_is_system_locked(self):
        # Check default lock state is unlocked
        assert not is_system_locked()

        # Check lock date in the future allows access
        self.forecast_edit_state.lock_date = datetime.today() + timedelta(days=1)
        self.forecast_edit_state.save()

        assert not is_system_locked()

        # Check lock date in past prevents access
        self.forecast_edit_state.lock_date = datetime.today() - timedelta(days=1)
        self.forecast_edit_state.save()

        assert is_system_locked()

    def is_system_closed(self):
        # Check default lock state is open
        assert not is_system_closed()

        # Set system to closed
        self.forecast_edit_state.closed = True
        self.forecast_edit_state.save()

        assert is_system_closed()

    def user_in_group(self):
        assert not user_in_group(self.test_user)

        new_group, _ = Group.objects.get_or_create(
            name='new_group',
        )

        new_group.user_set.add(self.test_user)

        assert user_in_group(self.test_user)

    def can_edit_at_least_one_cost_centre(self):
        assert not can_edit_at_least_one_cost_centre()

        # Assigns user to one cost centre
        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

        assert can_edit_at_least_one_cost_centre()


class TestCanForecastBeEdited(PermissionTestBase):
    def setUp(self):
        super().setUp()

        self.test_user, _ = get_user_model().objects.get_or_create(
            username="test_user",
            email="test@test.com",
        )
        self.test_user.set_password("test_password")
        self.test_user.save()

    def lock(self):
        self.forecast_edit_state.lock_date = datetime.today() - timedelta(days=1)
        self.forecast_edit_state.save()

    def close(self):
        self.forecast_edit_state.closed = True
        self.forecast_edit_state.save()

    def test_super_user(self):
        self.test_user.is_superuser = True
        self.test_user.save()

        assert can_forecast_be_edited(self.test_user)

        self.close()
        assert can_forecast_be_edited(self.test_user)

        self.lock()
        assert can_forecast_be_edited(self.test_user)

    def test_close(self):
        assert can_forecast_be_edited(self.test_user)

        self.close()
        assert not can_forecast_be_edited(self.test_user)

    def test_lock(self):
        assert can_forecast_be_edited(self.test_user)

        self.lock()
        assert not can_forecast_be_edited(self.test_user)

    def test_can_edit_whilst_locked_permission(self):
        self.lock()
        assert not can_forecast_be_edited(self.test_user)

        self.assign_permission("can_edit_whilst_locked")

        assert can_forecast_be_edited(self.test_user)

        self.close()
        assert can_forecast_be_edited(self.test_user)

        self.lock()
        assert can_forecast_be_edited(self.test_user)

    def test_can_edit_whilst_closed_permission(self):
        self.close()
        assert not can_forecast_be_edited(self.test_user)

        self.assign_permission("can_edit_whilst_closed")

        assert can_forecast_be_edited(self.test_user)
        self.lock()

        assert not can_forecast_be_edited(self.test_user)

    def test_unlocked_user(self):
        assert can_forecast_be_edited(self.test_user)

        self.lock()
        assert not can_forecast_be_edited(self.test_user)

        UnlockedForecastEditorFactory(
            user=self.test_user,
        )

        assert can_forecast_be_edited(self.test_user)


class TestCanEditCostCentre(BaseTestCase, PermissionTestBase):
    def setUp(self):
        super().setUp()

    def test_super_user(self):
        assert not can_edit_cost_centre(
            self.test_user,
            self.cost_centre_code,
        )

        self.test_user.is_superuser = True
        self.test_user.save()

        assert can_edit_cost_centre(
            self.test_user,
            self.cost_centre,
        )

    def test_basic_user_edit_permission(self):
        assert not can_edit_cost_centre(
            self.test_user,
            self.cost_centre_code,
        )

        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

        assert can_edit_cost_centre(
            self.test_user,
            self.cost_centre_code,
        )

    def test_edit_forecast_all_cost_centres_permission(self):
        assert not can_edit_cost_centre(
            self.test_user,
            self.cost_centre_code,
        )

        self.assign_permission("edit_forecast_all_cost_centres")

        assert can_edit_cost_centre(
            self.test_user,
            self.cost_centre_code,
        )
