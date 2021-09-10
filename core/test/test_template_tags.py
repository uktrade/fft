from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from core.templatetags.util import has_end_of_month_archive_permissions
from core.test.test_base import TEST_EMAIL


class ArchivePermissionsTest(TestCase):
    def test_can_archive_end_of_month(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email=TEST_EMAIL
        )

        assert not has_end_of_month_archive_permissions(test_user)

        group, created = Group.objects.get_or_create(
            name='Finance Administrator'  # #PS-IGNORE
        )
        test_user.groups.add(group)
        test_user.save()

        # Bust permissions cache (refresh_from_db does not work)
        test_user, _ = get_user_model().objects.get_or_create(
            email=TEST_EMAIL
        )

        assert has_end_of_month_archive_permissions(test_user)
