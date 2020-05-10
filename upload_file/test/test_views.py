import os
import re
from unittest.mock import MagicMock

from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.test import (
    TestCase,
    override_settings,
)
from django.urls import reverse

from core.test.test_base import RequestFactoryBase

from upload_file.test.factories import FileUploadFactory
from upload_file.views import UploadedView


# Set file upload handlers back to default as
# we need to remove S3 interactions for test purposes
@override_settings(
    FILE_UPLOAD_HANDLERS=[
        "django.core.files.uploadhandler.MemoryFileUploadHandler",
        "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    ],
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
)
class UploadedViewTests(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        file_mock = MagicMock(spec=File)
        file_mock.name = "test_a_unique_name.txt"
        self.file_name_regex = "test_a_unique_name(.*).txt"

        file_upload = FileUploadFactory.create(
            uploading_user=self.test_user, document_file=file_mock,
        )
        self.file_mock_name = file_upload.document_file.name

    def test_upload_view(self):
        assert not self.test_user.has_perm("forecast.can_upload_files")

        uploaded_files_url = reverse("uploaded_files",)

        # Should have been redirected (no permission)
        with self.assertRaises(PermissionDenied):
            self.factory_get(
                uploaded_files_url, UploadedView,
            )

        can_upload_files = Permission.objects.get(codename="can_upload_files",)
        self.test_user.user_permissions.add(can_upload_files)
        self.test_user.save()

        resp = self.factory_get(uploaded_files_url, UploadedView,)

        # Should have been permission now
        self.assertEqual(resp.status_code, 200)
        res = re.search(self.file_name_regex, resp.rendered_content,)
        # File name should be in response
        assert res is not None

        if os.path.exists(self.file_mock_name):
            os.remove(self.file_mock_name)
