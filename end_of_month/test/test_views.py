from django.contrib.auth.models import (
    Group,
)
from django.urls import reverse

from core.test.test_base import BaseTestCase


class ViewPermissionsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

    def test_user_has_no_end_of_month_archive_permission(self):
        end_of_month_url = reverse("end_of_month")

        response = self.client.get(end_of_month_url)

        assert response.status_code == 403

    def test_user_has_end_of_month_archive_permission(self):
        self.group, created = Group.objects.get_or_create(name='Finance Administrator')
        self.test_user.groups.add(self.group)

        end_of_month_url = reverse("end_of_month")

        resp = self.client.get(end_of_month_url)

        assert resp.status_code == 200
