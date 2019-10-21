from guardian.shortcuts import assign_perm

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import (
    get_user_model,
)

from costcentre.test.factories import CostCentreFactory


class ViewPermissionsTest(TestCase):
    def setUp(self):
        self.cost_centre_code = 888812
        self.test_user_email = "test@test.com"
        self.test_password = "test_password"

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email
        )

        self.test_user.set_password(
            self.test_password
        )

    def test_edit_forecast_view(self):
        self.assertFalse(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

        self.client.force_login(
            user=self.test_user
        )

        resp = self.client.get(
            reverse('edit_forecast'),
            follow=True,
        )

        self.assertEqual(
            resp.status_code,
            200
        )

        self.assertRedirects(
            resp,
            reverse('costcentre'),
        )

        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre
        )
        assign_perm(
            "view_costcentre",
            self.test_user,
            self.cost_centre
        )

        self.assertTrue(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

        self.assertTrue(
            self.test_user.has_perm(
                "view_costcentre",
                self.cost_centre,
            )
        )

        self.client.force_login(
            user=self.test_user
        )

        resp = self.client.get(
            reverse('edit_forecast'),
        )

        # Should be allowed
        self.assertEqual(
            resp.status_code,
            200,
        )
