import os

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

    def tearDown(self):
        if os.path.exists(self.excel_file_name):
            os.remove(self.excel_file_name)

    def test_wrong_nac_type(self):
        data_dictionary = [
            {
                COST_CENTRE_CODE_INDEX: self.cost_centre_code,
                NAC_CODE_INDEX: self.natural_account_code_non_pay,
                PROGRAMME_CODE_INDEX: self.programme_code,
                PROJECT_CODE_INDEX: self.project_code1,
                MONTH1_INDEX: 0.123,
            },
        ]
        data_worksheet, self.excel_file_name = create_workbook(data_dictionary)
        file_upload_obj = FileUpload(
            document_file_name=self.excel_file_name,
            document_type=FileUpload.PROJECT_PERCENTAGE,
            file_location=FileUpload.LOCALFILE,
        )
        file_upload_obj.save()
        upload_project_percentage_from_file(data_worksheet, file_upload_obj)
        assert (
            f"Row 2 error: The budget category of "
            f"'{self.natural_account_code_non_pay}' is not the correct type"
            in file_upload_obj.user_error_message
        )

    def test_multiple_directorate(self):
        data_dictionary = [
            {
                COST_CENTRE_CODE_INDEX: self.cost_centre_code,
                NAC_CODE_INDEX: self.natural_account_code_pay,
                PROGRAMME_CODE_INDEX: self.programme_code,
                PROJECT_CODE_INDEX: self.project_code1,
                MONTH1_INDEX: 0.50,
            },
            {
                COST_CENTRE_CODE_INDEX: self.cost_centre_code_different_directorate,
                NAC_CODE_INDEX: self.natural_account_code_pay,
                PROGRAMME_CODE_INDEX: self.programme_code,
                PROJECT_CODE_INDEX: self.project_code1,
                MONTH1_INDEX: 0.30,
            },
        ]
        data_worksheet, self.excel_file_name = create_workbook(data_dictionary)

        file_upload_obj = FileUpload(
            document_file_name=self.excel_file_name,
            document_type=FileUpload.PROJECT_PERCENTAGE,
            file_location=FileUpload.LOCALFILE,
        )
        file_upload_obj.save()
        upload_project_percentage_from_file(data_worksheet, file_upload_obj)

        assert (
            f"Row 3 error: Cost centre "
            f"'{self.cost_centre_code_different_directorate}' is not part"
            in file_upload_obj.user_error_message
        )

    def test_percentage_too_high(self):
        data_dictionary = [
            {
                COST_CENTRE_CODE_INDEX: self.cost_centre_code,
                NAC_CODE_INDEX: self.natural_account_code_pay,
                PROGRAMME_CODE_INDEX: self.programme_code,
                PROJECT_CODE_INDEX: self.project_code1,
                MONTH1_INDEX: 1.1,
            },
        ]
        data_worksheet, self.excel_file_name = create_workbook(data_dictionary)

        file_upload_obj = FileUpload(
            document_file_name=self.excel_file_name,
            document_type=FileUpload.PROJECT_PERCENTAGE,
            file_location=FileUpload.LOCALFILE,
        )
        file_upload_obj.save()
        upload_project_percentage_from_file(data_worksheet, file_upload_obj)

        assert (
            "Row 2 error: Value higher than 100% in cell"
            in file_upload_obj.user_error_message
        )

    def test_total_percentage_too_high(self):
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
                MONTH1_INDEX: 0.35,
            },
        ]
        data_worksheet, self.excel_file_name = create_workbook(data_dictionary)

        file_upload_obj = FileUpload(
            document_file_name=self.excel_file_name,
            document_type=FileUpload.PROJECT_PERCENTAGE,
            file_location=FileUpload.LOCALFILE,
        )
        file_upload_obj.save()
        upload_project_percentage_from_file(data_worksheet, file_upload_obj)

        assert (
            "The sum of the percentages is higher than 100%"
            in file_upload_obj.user_error_message
        )

    def test_total_percentage_too_low(self):
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
                MONTH1_INDEX: 0.2,
            },
        ]
        data_worksheet, self.excel_file_name = create_workbook(data_dictionary)

        file_upload_obj = FileUpload(
            document_file_name=self.excel_file_name,
            document_type=FileUpload.PROJECT_PERCENTAGE,
            file_location=FileUpload.LOCALFILE,
        )
        file_upload_obj.save()
        upload_project_percentage_from_file(data_worksheet, file_upload_obj)

        assert (
            "The sum of the percentages is lower than 100%"
            in file_upload_obj.user_error_message
        )
