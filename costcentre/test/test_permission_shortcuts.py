from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase


class PermissionShortcutsTest(
    TestCase,
):
    def setUp(self):
        self.test_user, created = get_user_model().objects.get_or_create(
            email='test@test.com'
        )

    def test_finance_admin_perm(self):
        self.group, created = Group.objects.get_or_create(name='Finance Administrator')
        self.test_user.groups.add(self.group)

        assert self.test_user.has_perm("costcentre.change_costcentre")
        assert self.test_user.has_perm("costcentre.edit_forecast_all_cost_centres")
        assert self.test_user.has_perm("costcentre.change_directorate")
        assert self.test_user.has_perm("costcentre.add_directorate")
        assert self.test_user.has_perm("costcentre.change_departmentalgroup")
        assert self.test_user.has_perm("costcentre.add_departmentalgroup")
        assert self.test_user.has_perm("costcentre.change_bsceemail")
        assert self.test_user.has_perm("costcentre.add_bsceemail")
        assert self.test_user.has_perm("costcentre.change_businesspartner")
        assert self.test_user.has_perm("costcentre.add_businesspartner")

    def test_fbp_perm(self):
        self.group, created = Group.objects.get_or_create(
            name='Finance Business Partner/BSCE')
        self.test_user.groups.add(self.group)

        assert self.test_user.has_perm("costcentre.change_costcentre")

        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.edit_forecast_all_cost_centres",
            )
        )
        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.change_directorate",
            )
        )
        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.add_directorate",
            )
        )
        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.change_departmentalgroup",
            )
        )
        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.add_departmentalgroup",
            )
        )
        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.change_bsceemail",
            )
        )
        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.add_bsceemail",
            )
        )
        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.change_businesspartner",
            )
        )
        self.assertFalse(
            self.test_user.has_perm(
                "costcentre.add_businesspartner",
            )
        )
