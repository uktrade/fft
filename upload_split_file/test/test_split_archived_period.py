import os

from django.utils import timezone

from end_of_month.end_of_month_actions import get_end_of_month
from upload_file.models import FileUpload
from upload_split_file.import_project_percentage import (
    upload_project_percentage_from_file,
)
from upload_split_file.test.test_utils import (
    COST_CENTRE_CODE_INDEX,
    MONTH1_INDEX,
    NAC_CODE_INDEX,
    PROGRAMME_CODE_INDEX,
    PROJECT_CODE_INDEX,
    SplitDataSetup,
    create_workbook,
)


class ImportPercentageTest(SplitDataSetup):
    def setUp(self):
        super().setUp()
        end_of_month_obj = get_end_of_month(2)
        end_of_month_obj.archived = True
        end_of_month_obj.archived_date = timezone.now()
        end_of_month_obj.save()

    def tearDown(self):
        if os.path.exists(self.excel_file_name):
            os.remove(self.excel_file_name)

    def test_dont_split_archived_month(self):
        data_dictionary = [
            {
                COST_CENTRE_CODE_INDEX: self.cost_centre_code,
                NAC_CODE_INDEX: self.natural_account_code_pay,
                PROGRAMME_CODE_INDEX: self.programme_code,
                PROJECT_CODE_INDEX: self.project_code1,
                MONTH1_INDEX: 0.7,
            },
            {
                COST_CENTRE_CODE_INDEX: self.cost_centre_code,
                NAC_CODE_INDEX: self.natural_account_code_pay,
                PROGRAMME_CODE_INDEX: self.programme_code,
                PROJECT_CODE_INDEX: self.project_code2,
                MONTH1_INDEX: 0.3,
            },
        ]
        data_worksheet, self.excel_file_name = create_workbook(data_dictionary)

        file_upload_obj = FileUpload(
            document_file_name=self.excel_file_name,
            document_type=FileUpload.PROJECT_PERCENTAGE,
            file_location=FileUpload.LOCALFILE,
        )
        file_upload_obj.save()
        upload_project_percentage_from_file(data_worksheet, file_upload_obj, False)

        assert file_upload_obj.error_count == 1
        assert "no data specified" in file_upload_obj.user_error_message

    def test_split_archived_month(self):
        data_dictionary = [
            {
                COST_CENTRE_CODE_INDEX: self.cost_centre_code,
                NAC_CODE_INDEX: self.natural_account_code_pay,
                PROGRAMME_CODE_INDEX: self.programme_code,
                PROJECT_CODE_INDEX: self.project_code1,
                MONTH1_INDEX: 0.7,
            },
            {
                COST_CENTRE_CODE_INDEX: self.cost_centre_code,
                NAC_CODE_INDEX: self.natural_account_code_pay,
                PROGRAMME_CODE_INDEX: self.programme_code,
                PROJECT_CODE_INDEX: self.project_code2,
                MONTH1_INDEX: 0.3,
            },
        ]
        data_worksheet, self.excel_file_name = create_workbook(data_dictionary)

        file_upload_obj = FileUpload(
            document_file_name=self.excel_file_name,
            document_type=FileUpload.PROJECT_PERCENTAGE,
            file_location=FileUpload.LOCALFILE,
        )
        file_upload_obj.save()
        upload_project_percentage_from_file(data_worksheet, file_upload_obj, True)

        assert file_upload_obj.error_count == 0
