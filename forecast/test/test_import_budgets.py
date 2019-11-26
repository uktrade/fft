import os
from typing import (
    Dict,
    TypeVar,
)
from zipfile import BadZipFile

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.test import RequestFactory, TestCase

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear

from costcentre.test.factories import (
    CostCentreFactory,
    DirectorateFactory,
)

from forecast.import_budgets import (
    EXPECTED_BUDGET_HEADERS,
    copy_uploaded_budget,
    upload_budget_from_file,
)
from forecast.import_utils import (
    UploadFileDataError,
    UploadFileFormatError,
)
from forecast.models import (
    Budget,
    FinancialPeriod,
    UploadingBudgets,
)

from upload_file.models import FileUpload

TEST_COST_CENTRE = 109189
TEST_VALID_NATURAL_ACCOUNT_CODE = 52191003
TEST_NOT_VALID_NATURAL_ACCOUNT_CODE = 92191003
TEST_PROGRAMME_CODE = '310940'


class ImportBudgetsTest(TestCase):
    def setUp(self):
        self.test_year = 2019
        self.test_period = 9

        self.factory = RequestFactory()
        self.cost_centre_code = TEST_COST_CENTRE
        self.valid_natural_account_code = TEST_VALID_NATURAL_ACCOUNT_CODE
        self.not_valid_natural_account_code = TEST_NOT_VALID_NATURAL_ACCOUNT_CODE
        self.programme_code = TEST_PROGRAMME_CODE
        self.test_amount = 100
        self.directorate_obj = DirectorateFactory.create(
            directorate_code='T123'
        )
        CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code,
            directorate=self.directorate_obj
        )
        NaturalCodeFactory.create(
            natural_account_code=self.valid_natural_account_code,
            used_for_budget=True
        )
        NaturalCodeFactory.create(
            natural_account_code=self.not_valid_natural_account_code
        )
        ProgrammeCodeFactory.create(
            programme_code=self.programme_code
        )

        ProgrammeCodeFactory.create(
            programme_code='333333'
        )

        self.year_obj = FinancialYear.objects.get(financial_year=2019)

        self.test_user_email = "test@test.com"
        self.test_password = "password"
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email,
        )

        self.test_user.set_password(self.test_password)

    def test_upload_budget_invalid_nac(self):
        self.assertEqual(
            UploadingBudgets.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        self.assertEqual(
            UploadingBudgets.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )


    def test_upload_budget_report(self):
        # Check that BadZipFile is raised on
        # supply of incorrect file format
        bad_file_type_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/bad_file_type.csv',
            ),
            uploading_user=self.test_user,
        )
        bad_file_type_upload.save()
        with self.assertRaises(BadZipFile):
            upload_budget_from_file(
                bad_file_type_upload,
                self.test_year,
            )

        bad_title_file_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/budget_upload_bad_header.xlsx',
            ),
            uploading_user=self.test_user,
        )
        bad_title_file_upload.save()

        with self.assertRaises(UploadFileFormatError):
            upload_budget_from_file(
                bad_title_file_upload,
                self.test_year,
            )

        self.assertEqual(
            Budget.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        self.assertEqual(
            UploadingBudgets.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        cost_centre_code_1 = 888888
        CostCentreFactory.create(
            cost_centre_code=cost_centre_code_1,
            directorate=self.directorate_obj
        )


        bad_file_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/upload_bad_data.xlsx',
            ),
            uploading_user=self.test_user,
        )
        bad_file_upload.save()

        with self.assertRaises(UploadFileDataError):
            upload_budget_from_file(
                bad_file_upload,
                self.test_year,
            )

        self.assertEqual(
            Budget.objects.filter(
                cost_centre=cost_centre_code_1
            ).count(),
            1,
        )

        good_file_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/upload_test.xlsx',
            ),
            uploading_user=self.test_user,
        )
        good_file_upload.save()

        upload_budget_from_file(
            good_file_upload,
            self.test_year,
        )
        # Check that existing figures for the same period have been deleted
        self.assertEqual(
            Budget.objects.filter(
                cost_centre=cost_centre_code_1
            ).count(),
            0,
        )
        # Check for existence of monthly figures
        self.assertEqual(
            Budget.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            4,
        )
        result = Budget.objects.filter(
            cost_centre=self.cost_centre_code
        ).aggregate(total=Sum('amount'))

        # Check that figures have correct values
        self.assertEqual(
            result['total'],
            1000000,
        )

        self.assertTrue(
            FinancialPeriod.objects.get(
                period_calendar_code=self.test_period
            ).actual_loaded
        )

