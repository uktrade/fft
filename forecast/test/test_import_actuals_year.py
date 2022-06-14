from django.contrib.auth.models import (
     Permission,
)
from django.urls import reverse

from core.test.test_base import BaseTestCase

from core.utils.generic_helpers import (
    get_current_financial_year,
    get_financial_year_obj,
    get_year_display,
)


class UploadActualsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.current_year = get_current_financial_year()
        # Make sure that at least one year in the future exists
        get_financial_year_obj(self.current_year+1)
        can_upload_files = Permission.objects.get(
            codename='can_upload_files'
        )
        self.test_user.user_permissions.add(can_upload_files)
        self.test_user.save()



    def test_upload_actuals_view(self):
        assert not self.test_user.has_perm("forecast.can_view_forecasts")
        uploaded_actuals_url = reverse(
            "upload_actuals_file",
        )
        response = self.client.get(
            uploaded_actuals_url,
        )
        self.assertEqual(response.status_code, 200)
        current_year_display = get_year_display(self.current_year)
        self.assertContains(response, current_year_display)
        next_year_display = get_year_display(self.current_year+1)
        self.assertNotContains(response, next_year_display)