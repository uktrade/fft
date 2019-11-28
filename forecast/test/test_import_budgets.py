import os
from zipfile import BadZipFile

from django.contrib.auth import get_user_model
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
    upload_budget_from_file,
)
from forecast.import_utils import (
    UploadFileDataError,
    UploadFileFormatError,
)
from forecast.models import (
    Budget,
    FinancialPeriod,
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
        self.cost_centre_code_1 = 888888
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
        CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code_1,
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

        bad_header_file_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/budget_upload_bad_header.xlsx',
            ),
            uploading_user=self.test_user,
        )
        bad_header_file_upload.save()

        with self.assertRaises(UploadFileFormatError):
            upload_budget_from_file(
                bad_header_file_upload,
                self.test_year,
            )
        # Check that the error is raised, and no data is uploaded
        bad_file_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/budget_upload_bad_data.xlsx',
            ),
            uploading_user=self.test_user,
        )
        bad_file_upload.save()

        self.assertEqual(
            Budget.objects.all().count(),
            0,
        )
        with self.assertRaises(UploadFileDataError):
            upload_budget_from_file(
                bad_file_upload,
                self.test_year,
            )
        self.assertEqual(
            Budget.objects.all().count(),
            0,
        )

        good_file_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/budget_upload_test.xlsx',
            ),
            uploading_user=self.test_user,
        )
        good_file_upload.save()

        upload_budget_from_file(
            good_file_upload,
            self.test_year,
        )

        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            Budget.objects.filter(
                financial_year=self.test_year
            ).count(),
            24,
        )
        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            Budget.objects.filter(
                financial_year=self.test_year,
                cost_centre=self.cost_centre_code
            ).count(),
            12,
        )
        # Check that figures for same budgets are added together
        self.assertEqual(
            Budget.objects.filter(
                financial_year=self.test_year,
                cost_centre=self.cost_centre_code,
                financial_period=1,
            ).first().amount,
            1100,
        )
        self.assertEqual(
            Budget.objects.filter(
                financial_year=self.test_year,
                cost_centre=self.cost_centre_code,
                financial_period=12,
            ).first().amount,
            2200,
        )

    def test_upload_budget_with_actuals(self):
        self.assertEqual(
            Budget.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        actual_month = 4
        FinancialPeriod.objects.filter(financial_period_code=actual_month). \
            update(actual_loaded=True)

        good_file_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/budget_upload_test.xlsx',
            ),
            uploading_user=self.test_user,
        )
        good_file_upload.save()

        upload_budget_from_file(
            good_file_upload,
            self.test_year,
        )

        self.assertEqual(
            Budget.objects.filter(
                financial_year=self.test_year
            ).count(),
            16,
        )
        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            Budget.objects.filter(
                financial_year=self.test_year,
                cost_centre=self.cost_centre_code
            ).count(),
            8,
        )
        # Check that there are no entry for the actual periods
        for period in range(1, actual_month + 1):
            self.assertEqual(
                Budget.objects.filter(
                    financial_year=self.test_year,
                    cost_centre=self.cost_centre_code,
                    financial_period=period,
                ).first(),
                None,
            )
        self.assertEqual(
            Budget.objects.filter(
                financial_year=self.test_year,
                cost_centre=self.cost_centre_code,
                financial_period=12,
            ).first().amount,
            2200,
        )
