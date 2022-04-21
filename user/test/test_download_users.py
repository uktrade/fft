from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from core.test.test_base import TEST_EMAIL

from user.download_users import download_users_queryset

class DownloadUserTest(TestCase):
    def setUp(self):
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=TEST_EMAIL
        )
        self.group, _ = Group.objects.get_or_create(name='test role')

    def test_user_no_role(self):
        queryset = download_users_queryset()
        assert queryset.count() == 0

    def test_user_with_role(self):
        self.test_user.groups.add(self.group)
        queryset = download_users_queryset()
        assert queryset.count() == 1

    def test_user_not_active_with_role(self):
        self.test_user.groups.add(self.group)
        self.test_user.is_active = False
        self.test_user.save()
        queryset = download_users_queryset()
        assert queryset.count() == 0


