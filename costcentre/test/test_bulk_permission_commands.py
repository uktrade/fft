from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from core.test.test_base import TEST_EMAIL

from costcentre.test.factories import CostCentreFactory, DirectorateFactory

from forecast.permission_shortcuts import assign_perm

FIRST_COST_CENTRE_CODE=888810
LAST_COST_CENTRE_CODE=888820


class CostCentrePermissionsCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

        directorate = DirectorateFactory.create()
        test_password = "test_password"

        for cc in range (FIRST_COST_CENTRE_CODE, LAST_COST_CENTRE_CODE):
            cost_centre_obj = CostCentreFactory.create(
                cost_centre_code=cc,
                directorate=directorate
            )
        self.directorate_code = directorate.directorate_code
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=TEST_EMAIL
        )

        self.test_user.set_password(test_password)
        self.test_user.save()

    def test_add_directorate_permission(self):
        # for cc in range(FIRST_COST_CENTRE_CODE, LAST_COST_CENTRE_CODE):
        #     self.assertFalse(self.test_user.has_perm(
        #         "change_costcentre",
        #         cc)
        #     )
        call_command(
            "add_user_to_cost_centre",
            email=self.test_user.email,
            cost_centre_code=FIRST_COST_CENTRE_CODE,
            stdout=self.out,
        )

        # call_command(
        #     "directorate_permission",
        #     email=self.test_user.email,
        #     directorate_code=self.directorate_code,
        #     stdout=self.out,
        # )

        for cc in range(FIRST_COST_CENTRE_CODE, FIRST_COST_CENTRE_CODE+1):
            print(f"user {self.test_user.id} cc {cc} permission"
                  f" {self.test_user.has_perm('change_costcentre', cc)}")
            call_command(
                "add_user_to_cost_centre",
                email=self.test_user.email,
                cost_centre_code=cc,
                stdout=self.out,
            )
            print(f"AFTER user {self.test_user.id} cc {cc} permission"
                  f" {self.test_user.has_perm('change_costcentre', cc)}")

            # self.assertFalse(self.test_user.has_perm(
            #     "change_costcentre",
            #     cc)
            # )

