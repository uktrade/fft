from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group,
)
from django.core.exceptions import PermissionDenied
from django.test import (
    TestCase,
)
from django.urls import reverse

from core.test.test_base import RequestFactoryBase

from end_of_month.views.end_of_month_archive import EndOfMonthProcessView


class ViewPermissionsTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.test_user, created = get_user_model().objects.get_or_create(
            email='test@test.com'
        )

    def test_user_has_no_end_of_month_archive_permission(self):
        end_of_month_url = reverse(
            "end_of_month",
        )

        with self.assertRaises(PermissionDenied):
            self.factory_get(
                end_of_month_url,
                EndOfMonthProcessView,
            )

    def test_user_has_end_of_month_archive_permission(self):
        self.group, created = Group.objects.get_or_create(name='Finance Administrator')
        self.test_user.groups.add(self.group)

        end_of_month_url = reverse(
            "end_of_month",
        )

        resp = self.factory_get(
            end_of_month_url,
            EndOfMonthProcessView,
        )

        assert resp.status_code == 200
