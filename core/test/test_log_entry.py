from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from core.test.test_base import TEST_EMAIL


class LogEntryTest(TestCase):
    def setUp(self):
        self.test_user, created = get_user_model().objects.get_or_create(
            email=TEST_EMAIL
        )

    def finance_admin_view_log_entry(self):
        self.group, created = Group.objects.get_or_create(name='Finance Administrator')
        self.test_user.groups.add(self.group)

        assert self.test_user.has_perm("view_logentry")
