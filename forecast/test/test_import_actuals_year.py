from bs4 import BeautifulSoup

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
        self.future_financial_year_display = get_financial_year_obj(get_current_financial_year() +1).financial_year_display
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
        self.assertNotContains(response, self.future_financial_year_display)