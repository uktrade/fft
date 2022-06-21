from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from core.test.test_base import TEST_EMAIL

from costcentre.models import CostCentre
from costcentre.test.factories import CostCentreFactory, DepartmentalGroupFactory, DirectorateFactory


FIRST_COST_CENTRE_CODE = 888810
LAST_COST_CENTRE_CODE = 888820


class DirectoratePermissionsCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

        test_password = "test_password"
        # Cost centre in a different directorate.
        self.other_cost_centre = CostCentreFactory.create(
            directorate=DirectorateFactory.create(directorate_code="AAAA1")
        )

        self.directorate_code = "DDDD1"
        directorate = DirectorateFactory.create(directorate_code=self.directorate_code)
        for cc in range(FIRST_COST_CENTRE_CODE, LAST_COST_CENTRE_CODE):
            CostCentreFactory.create(cost_centre_code=cc, directorate=directorate)
        self.test_user, _ = get_user_model().objects.get_or_create(email=TEST_EMAIL)
        self.test_user.set_password(test_password)
        self.test_user.save()

    def test_add_directorate_permission(self):
        for cc in range(FIRST_COST_CENTRE_CODE, LAST_COST_CENTRE_CODE):
            self.assertFalse(
                self.test_user.has_perm(
                    "change_costcentre", CostCentre.objects.get(cost_centre_code=cc)
                )
            )

        self.assertFalse(
            self.test_user.has_perm("change_costcentre", self.other_cost_centre)
        )

        call_command(
            "add_user_to_directorate",
            email=self.test_user.email,
            directorate_code=self.directorate_code,
            stdout=self.out,
        )

        for cc in range(FIRST_COST_CENTRE_CODE, LAST_COST_CENTRE_CODE):
            self.assertTrue(
                self.test_user.has_perm(
                    "change_costcentre", CostCentre.objects.get(cost_centre_code=cc)
                )
            )
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

        self.group_code = "GGGG1"
        # Cost centre in a different directorate.
        self.other_cost_centre = CostCentreFactory.create(
            directorate=DirectorateFactory.create(directorate_code="AAAA1")
        )

        self.directorate_code = "DDDD1"
        directorate = DirectorateFactory.create(directorate_code=self.directorate_code)
        for cc in range(FIRST_COST_CENTRE_CODE, LAST_COST_CENTRE_CODE):
            CostCentreFactory.create(cost_centre_code=cc, directorate=directorate)


    def test_add_directorate_permission(self):
        for cc in range(FIRST_COST_CENTRE_CODE, LAST_COST_CENTRE_CODE):
            self.assertFalse(
                self.test_user.has_perm(
                    "change_costcentre", CostCentre.objects.get(cost_centre_code=cc)
                )
            )

        self.assertFalse(
            self.test_user.has_perm("change_costcentre", self.other_cost_centre)
        )

        call_command(
            "add_user_to_directorate",
            email=self.test_user.email,
            directorate_code=self.directorate_code,
            stdout=self.out,
        )

        for cc in range(FIRST_COST_CENTRE_CODE, LAST_COST_CENTRE_CODE):
            self.assertTrue(
                self.test_user.has_perm(
                    "change_costcentre", CostCentre.objects.get(cost_centre_code=cc)
                )
            )
        # The user does not have permission for cost centre in different directorate
        self.assertFalse(
            self.test_user.has_perm("change_costcentre", self.other_cost_centre)
        )
