from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from core.test.test_base import TEST_COST_CENTRE, TEST_EMAIL
from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)
from forecast.permission_shortcuts import assign_perm


class CostCentrePermissionsCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

        self.cost_centre_code = TEST_COST_CENTRE
        self.test_user_email = TEST_EMAIL
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
        self.assertFalse(self.test_user.has_perm("change_costcentre", self.cost_centre))
        call_command(
            "add_user_to_cost_centre",
            email=self.test_user_email,
            cost_centre_code=self.cost_centre_code,
            stdout=self.out,
        )

        self.assertTrue(self.test_user.has_perm("change_costcentre", self.cost_centre))

    def test_remove_user_from_cost_centre(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

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

        self.assertTrue(self.test_user.has_perm("change_costcentre", self.cost_centre))

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
            "on the following cost centres:".format(self.test_user_email),
            out_value,
        )

        self.assertIn(str(self.cost_centre_code), out_value)


class DirectoratePermissionsCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

        test_password = "test_password"
        # Cost centre in a different directorate.
        self.other_cost_centre = CostCentreFactory.create(
            directorate=DirectorateFactory.create(directorate_code="AAAA1")
        )
        self.cc_list = []
        self.directorate_code = "DDDD1"
        directorate = DirectorateFactory.create(directorate_code=self.directorate_code)
        for cc in range(1, 10):
            self.cc_list.append(
                CostCentreFactory.create(cost_centre_code=cc, directorate=directorate)
            )

        self.test_user, _ = get_user_model().objects.get_or_create(email=TEST_EMAIL)
        self.test_user.set_password(test_password)
        self.test_user.save()

    def test_add_directorate_permission(self):
        for cc in self.cc_list:
            self.assertFalse(self.test_user.has_perm("change_costcentre", cc))

        self.assertFalse(
            self.test_user.has_perm("change_costcentre", self.other_cost_centre)
        )

        call_command(
            "add_user_to_directorate",
            email=self.test_user.email,
            directorate_code=self.directorate_code,
            stdout=self.out,
        )

        for cc in self.cc_list:
            self.assertTrue(self.test_user.has_perm("change_costcentre", cc))
        # The user does not have permission for cost centre in different directorate
        self.assertFalse(
            self.test_user.has_perm("change_costcentre", self.other_cost_centre)
        )


class GroupPermissionsCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

        self.test_user, _ = get_user_model().objects.get_or_create(email=TEST_EMAIL)
        self.test_user.set_password("test_password")
        self.test_user.save()
        self.cc_list = []

        self.group_code = "GGGG1"
        group = DepartmentalGroupFactory.create(group_code=self.group_code)
        for i in range(0, 3):
            directorate = DirectorateFactory.create(
                group=group, directorate_code=f"D99{i}"
            )
            for j in range(0, 10):
                cost_centre = CostCentreFactory.create(
                    directorate=directorate, cost_centre_code=f"9999{i}{j}"
                )
                self.cc_list.append(cost_centre)

        # Cost centre in a different group.
        self.other_cost_centre = []
        DepartmentalGroupFactory.create(group_code="G1000")
        for i in range(0, 3):
            directorate = DirectorateFactory.create(directorate_code=f"D88{i}")
            directorate.group_id = "G1000"
            directorate.save()
            for j in range(0, 10):
                cost_centre = CostCentreFactory.create(
                    directorate=directorate, cost_centre_code=f"8888{i}{j}"
                )
                self.other_cost_centre.append(cost_centre)

    def test_add_group_permission(self):
        for cc in self.other_cost_centre:
            self.assertFalse(self.test_user.has_perm("change_costcentre", cc))

        for cc in self.cc_list:
            self.assertFalse(self.test_user.has_perm("change_costcentre", cc))

        call_command(
            "add_user_to_group",
            email=self.test_user.email,
            group_code=self.group_code,
            stdout=self.out,
        )

        # The user does not have permission for cost centre in different group
        for cc in self.cc_list:
            self.assertTrue(self.test_user.has_perm("change_costcentre", cc))
        for cc in self.other_cost_centre:
            self.assertFalse(self.test_user.has_perm("change_costcentre", cc))
