from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from core.test.test_base import TEST_EMAIL
from treasurySS.admin import SubSegmentAdmin
from treasurySS.models import SubSegment


class AdminDownloadSusbsegmentTest(TestCase):
    def setUp(self):
        self.test_user, _ = get_user_model().objects.get_or_create(email=TEST_EMAIL)

    def test_download_subsegment(self):
        factory = RequestFactory()
        request = factory.get("/export-xls/")
        request.user = self.test_user
        ss = SubSegmentAdmin(SubSegment, None)
        response = ss.export_all_xls(request)
        assert response.status_code == 200
