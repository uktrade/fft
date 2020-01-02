from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from upload_file.templatetags.upload_permissions import (
    has_upload_permission,
)


class UploadPermissionTestTestCase(TestCase):
    def test_has_upload_permission(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert not has_upload_permission(test_user)

        can_upload_files = Permission.objects.get(
            codename='can_upload_files',
        )
        test_user.user_permissions.add(can_upload_files)
        test_user.save()

        # Bust permissions cache (refresh_from_db does not work)
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert has_upload_permission(test_user) is True
