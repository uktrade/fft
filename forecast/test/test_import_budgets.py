import os
from unittest.mock import MagicMock, patch
from zipfile import BadZipFile

from django.contrib.auth.models import Group
from django.core.files import File
from django.test import override_settings
from django.urls import reverse

from chartofaccountDIT.test.factories import NaturalCodeFactory, ProgrammeCodeFactory
from core.models import FinancialYear
from core.test.test_base import BaseTestCase
from costcentre.test.factories import CostCentreFactory, DirectorateFactory
from forecast.import_budget_or_forecast import upload_budget_from_file
from forecast.models import BudgetMonthlyFigure, FinancialPeriod
from forecast.utils.import_helpers import UploadFileFormatError
from upload_file.models import FileUpload


TEST_COST_CENTRE = 109189
TEST_VALID_NATURAL_ACCOUNT_CODE = 52191003
TEST_NOT_VALID_NATURAL_ACCOUNT_CODE = 92191003
TEST_PROGRAMME_CODE = "310940"


# Set file upload handlers back to default as
# we need to remove S3 interactions for test purposes
@override_settings(
    FILE_UPLOAD_HANDLERS=[
        "django.core.files.uploadhandler.MemoryFileUploadHandler",
        "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    ]
)
class ImportBudgetsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.test_year = 2019
        self.test_period = 9

        self.file_mock = MagicMock(spec=File)
        self.file_mock.name = "test.txt"

        self.cost_centre_code = TEST_COST_CENTRE
        self.cost_centre_code_1 = 888888
        self.valid_natural_account_code = TEST_VALID_NATURAL_ACCOUNT_CODE
        self.not_valid_natural_account_code = TEST_NOT_VALID_NATURAL_ACCOUNT_CODE
        self.programme_code = TEST_PROGRAMME_CODE
        self.test_amount = 100
        self.directorate_obj = DirectorateFactory.create(directorate_code="T123")
        CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code, directorate=self.directorate_obj
        )
        CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code_1, directorate=self.directorate_obj
        )

        NaturalCodeFactory.create(
            natural_account_code=self.valid_natural_account_code, used_for_budget=True
        )
        NaturalCodeFactory.create(
            natural_account_code=self.not_valid_natural_account_code
        )
        ProgrammeCodeFactory.create(programme_code=self.programme_code)

        ProgrammeCodeFactory.create(programme_code="333333")

        self.year_obj = FinancialYear.objects.get(financial_year=2019)

    def test_upload_budget_report(self):
        # Check that BadZipFile is raised on
        # supply of incorrect file format
        bad_file_type_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/bad_file_type.csv",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        bad_file_type_upload.save()
        with self.assertRaises(BadZipFile):
            upload_budget_from_file(
                bad_file_type_upload,
                self.test_year,
            )

        bad_header_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/budget_upload_bad_header.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        bad_header_file_upload.save()

        with self.assertRaises(UploadFileFormatError):
            upload_budget_from_file(
                bad_header_file_upload,
                self.test_year,
            )
        # Check that the error is raised, and no data is uploaded
        bad_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/budget_upload_bad_data.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        bad_file_upload.save()

        self.assertEqual(
            BudgetMonthlyFigure.objects.all().count(),
            0,
        )
        upload_budget_from_file(
            bad_file_upload,
            self.test_year,
        )
        self.assertEqual(bad_file_upload.status, FileUpload.PROCESSEDWITHERROR)
        self.assertEqual(
            BudgetMonthlyFigure.objects.all().count(),
            0,
        )

        good_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/budget_upload_test.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        good_file_upload.save()

        upload_budget_from_file(
            good_file_upload,
            self.test_year,
        )

        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            24,
        )
        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            12,
        )
        # Check that figures for same budgets are added together
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=1,
            )
            .first()
            .amount,
            1100,
        )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=12,
            )
            .first()
            .amount,
            2200,
        )

    def test_upload_budget_with_actuals(self):
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        actual_month = 4
        FinancialPeriod.objects.filter(financial_period_code=actual_month).update(
            actual_loaded=True
        )

        good_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/budget_upload_test.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        good_file_upload.save()

        upload_budget_from_file(
            good_file_upload,
            self.test_year,
        )

        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            16,
        )
        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            8,
        )
        # Check that there are no entry for the actual periods
        for period in range(1, actual_month + 1):
            self.assertEqual(
                BudgetMonthlyFigure.objects.filter(
                    financial_year=self.test_year,
                    financial_code__cost_centre=self.cost_centre_code,
                    financial_period=period,
                ).first(),
                None,
            )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=12,
            )
            .first()
            .amount,
            2200,
        )

    @override_settings(ASYNC_FILE_UPLOAD=False)
    @patch("forecast.views.upload_file.process_uploaded_file")
    def test_finance_admin_can_upload_budget(self, mock_process_uploaded_file):
        assert not self.test_user.groups.filter(name="Finance Administrator")

        uploaded_actuals_url = reverse("upload_budget_file")

        # Should have been redirected (no permission)
        resp = self.client.get(
            uploaded_actuals_url,
            follow=False,
        )

        assert resp.status_code == 403

        finance_admins = Group.objects.get(
            name="Finance Administrator",
        )
        finance_admins.user_set.add(self.test_user)
        finance_admins.save()

        resp = self.client.get(uploaded_actuals_url)

        # Should have been permission now
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            uploaded_actuals_url,
            data={
                "year": self.test_year,
                "file": self.file_mock,
            },
        )

        # Make sure upload was process was kicked off
        assert mock_process_uploaded_file.called

        # Should have been redirected to document upload  page
        self.assertEqual(resp.status_code, 302)
        assert resp.url == "/upload/files/"

        # Clean up file
        file_path = "uploaded/actuals/{}".format(self.file_mock.name)
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_budget_file_contains_dash(self):
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        actual_month = 4
        FinancialPeriod.objects.filter(financial_period_code=actual_month).update(
            actual_loaded=True
        )

        good_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/budget_upload_bad_dash.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        good_file_upload.save()

        upload_budget_from_file(
            good_file_upload,
            self.test_year,
        )

        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            16,
        )
        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            8,
        )
        # Check that there are no entry for the actual periods
        for period in range(1, actual_month + 1):
            self.assertEqual(
                BudgetMonthlyFigure.objects.filter(
                    financial_year=self.test_year,
                    financial_code__cost_centre=self.cost_centre_code,
                    financial_period=period,
                ).first(),
                None,
            )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=12,
            )
            .first()
            .amount,
            2200,
        )

    def test_budget_file_with_spaces_and_blanks(self):
        good_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/budget_upload_blank_data.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        good_file_upload.save()

        upload_budget_from_file(
            good_file_upload,
            self.test_year,
        )

        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            24,
        )
        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            12,
        )
        # Check that figures for same budgets are added together
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=1,
            )
            .first()
            .amount,
            1100,
        )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=12,
            )
            .first()
            .amount,
            2200,
        )

    def test_upload_budget_adj_columns(self):
        adj_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/budget_upload_adj_columns.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        adj_file_upload.save()

        upload_budget_from_file(
            adj_file_upload,
            self.test_year,
        )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            30,
        )

        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            15,
        )
        # Check that figures for same budgets are added together
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=13,
            )
            .first()
            .amount,
            1010000,
        )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=14,
            )
            .first()
            .amount,
            2020000,
        )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=15,
            )
            .first()
            .amount,
            3030000,
        )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.test_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=12,
            )
            .first()
            .amount,
            2200,
        )

    def test_upload_budget_zero_cost_centre(self):
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
        file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                "test_assets/budget_upload_zero_cost_centre_test.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        file_upload.save()

        upload_budget_from_file(
            file_upload,
            self.test_year,
        )
        # No budgets uploaded, because of zero cost centre code
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.test_year).count(),
            0,
        )
