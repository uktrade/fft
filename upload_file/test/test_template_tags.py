from django.contrib.auth import get_user_model
from django.test import TestCase

from upload_file.templatetags.upload_permissions import (
    has_upload_permission,
)
from upload_file.test.factories import UploadPermissionFactory


class UploadPermissionTestTestCase(TestCase):
    def test_has_upload_permission(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert not has_upload_permission(test_user)

        UploadPermissionFactory(
            user=test_user,
        )

        assert has_upload_permission(test_user) is True
