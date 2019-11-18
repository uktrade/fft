from django.contrib.auth import get_user_model
from django.test import TestCase

from forecast.test.factories import ForecastPermissionFactory

from upload_file.templatetags.upload_permissions import (
    has_upload_permission,
)


class UploadPermissionTestTestCase(TestCase):
    def test_has_upload_permission(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert not has_upload_permission(test_user)

        ForecastPermissionFactory(
            user=test_user,
            can_upload=True,
        )

        assert has_upload_permission(test_user) is True
