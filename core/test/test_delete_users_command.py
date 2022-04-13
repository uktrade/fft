from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from core.test.test_base import TEST_EMAIL

from costcentre.test.factories import CostCentreFactory

from forecast.permission_shortcuts import assign_perm

from core.remove_users import delete_user


class CostCentrePermissionsCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.first_name = "John"
        self.last_name = "Smith"

        self.cost_centre_code = 888812
        self.test_user_email = TEST_EMAIL
        self.test_password = "test_password"

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email,
            first_name=self.first_name,
            last_name=self.last_name,
        )

        self.test_user.is_superuser = True
        self.test_user.is_staff = True
        self.test_user.is_active = True
        self.test_user.save()

        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

    def test_delete_user(self):
        self.assertTrue(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

        delete_user(self.first_name, self.last_name)
        self.test_user.refresh_from_db()

        assert (
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
            == False
        )
        assert self.test_user.is_active == False
        assert self.test_user.is_staff == False
        assert self.test_user.is_superuser == False
