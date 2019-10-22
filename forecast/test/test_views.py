from guardian.shortcuts import assign_perm

from django.urls import reverse
from django.test import (
    RequestFactory,
    TestCase,
)
from django.contrib.auth import (
    get_user_model,
)

from costcentre.test.factories import CostCentreFactory
from forecast.views import EditForecastView


class ViewPermissionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

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

        request = self.factory.get(
            reverse('edit_forecast')
        )
        request.user = self.test_user

        resp = EditForecastView.as_view()(request)

        # Should have been redirected (no permission)
        self.assertEqual(resp.status_code, 302)

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

        request = self.factory.get(
            reverse('edit_forecast')
        )
        request.user = self.test_user

        resp = EditForecastView.as_view()(request)

        # Should be allowed
        self.assertEqual(
            resp.status_code,
            200,
        )
