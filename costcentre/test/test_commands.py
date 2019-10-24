from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from guardian.shortcuts import assign_perm

from costcentre.test.factories import CostCentreFactory


class CostCentrePermissionsCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

        self.cost_centre_code = 888812
        self.test_user_email = "test@test.com"
        self.test_password = "test_password"

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email
        )

        self.test_user.set_password(self.test_password)
        self.test_user.save()

    def test_add_user_to_cost_centre(self):
        self.assertFalse(self.test_user.has_perm(
            "change_costcentre",
            self.cost_centre)
        )
        call_command(
            "add_user_to_cost_centre",
            email=self.test_user_email,
            cost_centre_code=self.cost_centre_code,
            stdout=self.out,
        )

        self.assertTrue(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre
            )
        )

    def test_remove_user_from_cost_centre(self):
        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre
        )

        self.assertTrue(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

        call_command(
            "remove_user_from_cost_centre",
            email=self.test_user_email,
            cost_centre_code=self.cost_centre_code,
            stdout=self.out,
        )

        self.test_user.refresh_from_db()

        self.assertFalse(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

    def test_cost_centre_users(self):
        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

        self.assertTrue(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre
            )
        )

        call_command(
            "cost_centre_users",
            "--cost_centre_code={}".format(self.cost_centre_code),
            stdout=self.out,
        )

        out_value = self.out.getvalue()

        self.assertIn(
            "Users with permission to edit cost centre {}:".format(
                self.cost_centre_code
            ),
            out_value,
        )

        self.assertIn(self.test_user_email, out_value)

    def test_user_permissions(self):
        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

        self.assertTrue(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

        call_command(
            "user_permissions",
            "--email={}".format(self.test_user_email),
            stdout=self.out,
        )

        out_value = self.out.getvalue()

        self.assertIn(
            "User with email '{}' has permissions "
            "on the following cost centres:".format(
                self.test_user_email
            ),
            out_value,
        )

        self.assertIn(str(self.cost_centre_code), out_value)
