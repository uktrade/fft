from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import (
    TestCase,
)

from forecast.tasks import process_uploaded_file

from upload_file.models import FileUpload
from upload_file.test.factories import FileUploadFactory


class ProcessUploadTest(TestCase):
    def setUp(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        self.file_upload = FileUploadFactory(
            status=FileUpload.UNPROCESSED,
            document_type=FileUpload.ACTUALS,
            uploading_user=test_user,
        )

    @patch('forecast.tasks.get_s3_file_body')
    @patch('forecast.tasks.run_anti_virus')
    def test_process_uploaded_file_has_malware(
        self,
        mock_run_anti_virus,
        mock_get_s3_file_body,
    ):
        mock_run_anti_virus.return_value = {
            "malware": True
        }

        process_uploaded_file()

        self.file_upload.refresh_from_db()

        assert mock_get_s3_file_body.called
        assert mock_run_anti_virus.called
        assert self.file_upload.status == FileUpload.ERROR
        assert self.file_upload.user_error_message == "A virus was found in the file"

    @patch('forecast.tasks.get_s3_file_body')
    @patch('forecast.tasks.run_anti_virus')
    @patch('forecast.tasks.upload_trial_balance_report')
    def test_process_uploaded_file_no_malware_trial_balance(
        self,
        mock_upload_trial_balance_report,
        mock_run_anti_virus,
        mock_get_s3_file_body,
    ):
        mock_run_anti_virus.return_value = {
            "malware": False
        }
        mock_upload_trial_balance_report.return_value = True

        process_uploaded_file()
        self.file_upload.refresh_from_db()

        assert mock_get_s3_file_body.called
        assert mock_run_anti_virus.called
        assert mock_upload_trial_balance_report.called
        assert self.file_upload.status == FileUpload.PROCESSED

    @patch('forecast.tasks.get_s3_file_body')
    @patch('forecast.tasks.run_anti_virus')
    @patch('forecast.tasks.upload_budget_from_file')
    def test_process_uploaded_file_no_malware_budget(
        self,
        mock_upload_budget_from_file,
        mock_run_anti_virus,
        mock_get_s3_file_body,
    ):
        self.file_upload.document_type = FileUpload.BUDGET
        self.file_upload.save()

        mock_run_anti_virus.return_value = {
            "malware": False
        }
        mock_upload_budget_from_file.return_value = True

        process_uploaded_file()
        self.file_upload.refresh_from_db()

        assert mock_get_s3_file_body.called
        assert mock_run_anti_virus.called
        assert mock_upload_budget_from_file.called
        assert self.file_upload.status == FileUpload.PROCESSED
