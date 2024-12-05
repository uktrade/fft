import os

from django.test import override_settings

from chartofaccountDIT.models import ArchivedNaturalCode, NaturalCode
from chartofaccountDIT.test.factories import (
    HistoricalNaturalCodeFactory,
    NaturalCodeFactory,
)
from core.test.test_base import BaseTestCase
from import_chart_of_account.import_nac_cash_income_fields import upload_nac_fields
from upload_file.models import FileUpload


@override_settings(
    FILE_UPLOAD_HANDLERS=[
        "django.core.files.uploadhandler.MemoryFileUploadHandler",
        "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    ]
)
class ImportNACFieldsTest(BaseTestCase):
    def setUp(self):
        self.natural_account_code_1 = 12345678
        self.natural_account_code_2 = 92191003
        NaturalCodeFactory.create(natural_account_code=self.natural_account_code_1)
        NaturalCodeFactory.create(natural_account_code=self.natural_account_code_2)
        HistoricalNaturalCodeFactory.create(
            natural_account_code=self.natural_account_code_1, financial_year_id=2019
        )
        HistoricalNaturalCodeFactory.create(
            natural_account_code=self.natural_account_code_2, financial_year_id=2019
        )

    def test_import_nac_fields(self):
        natural_account_obj = NaturalCode.objects.get(
            natural_account_code=self.natural_account_code_1
        )
        self.assertIsNone(natural_account_obj.gross_income)
        assert natural_account_obj.cash_non_cash == NaturalCode.NOT_DEFINED

        natural_account_obj = NaturalCode.objects.get(
            natural_account_code=self.natural_account_code_2
        )
        self.assertIsNone(natural_account_obj.gross_income)
        assert natural_account_obj.cash_non_cash == NaturalCode.NOT_DEFINED

        # Check the archived data
        natural_account_obj = ArchivedNaturalCode.objects.get(
            natural_account_code=self.natural_account_code_1
        )
        self.assertIsNone(natural_account_obj.gross_income)
        assert natural_account_obj.cash_non_cash == NaturalCode.NOT_DEFINED

        natural_account_obj = ArchivedNaturalCode.objects.get(
            natural_account_code=self.natural_account_code_2
        )
        self.assertIsNone(natural_account_obj.gross_income)
        assert natural_account_obj.cash_non_cash == NaturalCode.NOT_DEFINED

        file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/import_nac_fields.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.OTHER,
        )
        file_upload.save()

        upload_nac_fields(
            file_upload,
        )
        natural_account_obj = NaturalCode.objects.get(
            natural_account_code=self.natural_account_code_1
        )
        assert natural_account_obj.gross_income == NaturalCode.GROSS
        assert natural_account_obj.cash_non_cash == NaturalCode.NON_CASH

        natural_account_obj = NaturalCode.objects.get(
            natural_account_code=self.natural_account_code_2
        )
        assert natural_account_obj.gross_income == NaturalCode.INCOME
        assert natural_account_obj.cash_non_cash == NaturalCode.CASH

        # Check the archived data
        natural_account_obj = ArchivedNaturalCode.objects.get(
            natural_account_code=self.natural_account_code_1
        )
        assert natural_account_obj.gross_income == NaturalCode.GROSS
        assert natural_account_obj.cash_non_cash == NaturalCode.NON_CASH

        natural_account_obj = ArchivedNaturalCode.objects.get(
            natural_account_code=self.natural_account_code_2
        )
        assert natural_account_obj.gross_income == NaturalCode.INCOME
        assert natural_account_obj.cash_non_cash == NaturalCode.CASH
