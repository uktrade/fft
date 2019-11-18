import os
from unittest.mock import MagicMock

from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from core.test.test_base import RequestFactoryBase

from upload_file.models import (
    UploadPermission,
)
from upload_file.test.factories import (
    FileUploadFactory,
    UploadPermissionFactory,
)
from upload_file.views import UploadedView


class UploadedViewTests(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.file_mock = MagicMock(spec=File)
        self.file_mock.name = 'test.txt'

        self.file_upload = FileUploadFactory.create(
            uploading_user=self.test_user,
            document_file=self.file_mock,
        )

    def test_upload_view(self):
        upload_permission_count = UploadPermission.objects.all().count()
        self.assertEqual(upload_permission_count, 0)

        uploaded_files_url = reverse(
            "uploaded_files",
        )

        # Should have been redirected (no permission)
        with self.assertRaises(PermissionDenied):
            self.factory_get(
                uploaded_files_url,
                UploadedView,
            )

        UploadPermissionFactory.create(
            user=self.test_user,
        )

        resp = self.factory_get(
            uploaded_files_url,
            UploadedView,
        )

        # Should have been permission now
        self.assertEqual(resp.status_code, 200)

        # File name should be in response
        assert self.file_mock.name in resp.rendered_content

        # Clean up file
        file_path = 'uploaded/actuals/{}'.format(
            self.file_mock.name
        )
        if os.path.exists(file_path):
            os.remove(file_path)
