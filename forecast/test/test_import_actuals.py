import os
from datetime import datetime
from unittest.mock import MagicMock, patch
from zipfile import BadZipFile

from django.contrib.auth.models import (
    Group,
    Permission,
)
from django.core.files import File
from django.db.models import Sum
from django.test import (
    override_settings,
)
from django.urls import reverse

from chartofaccountDIT.models import (
    NaturalCode,
    ProgrammeCode,
)
from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import BaseTestCase
from core.utils.excel_test_helpers import (
    FakeCell,
    FakeWorkSheet
)

from costcentre.models import (
    CostCentre,
)
from costcentre.test.factories import (
    CostCentreFactory,
    DirectorateFactory,
)

from forecast.import_actuals import (
    CORRECT_TRIAL_BALANCE_TITLE,
    CORRECT_TRIAL_BALANCE_WORKSHEET_NAME,
    GENERIC_PROGRAMME_CODE,
    MONTH_CELL,
    TITLE_CELL,
    UploadFileFormatError,
    check_trial_balance_format,
    copy_actuals_to_monthly_figure,
    save_trial_balance_row,
    upload_trial_balance_report,
)
from forecast.models import (
    ActualUploadMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.utils.import_helpers import (
    CheckFinancialCode,
    VALID_ECONOMIC_CODE_LIST,
)

from upload_file.models import FileUpload

TEST_COST_CENTRE = 109189
TEST_VALID_NATURAL_ACCOUNT_CODE = 52191003
TEST_NOT_VALID_NATURAL_ACCOUNT_CODE = 92191003
TEST_PROGRAMME_CODE = '310940'


# Set file upload handlers back to default as
# we need to remove S3 interactions for test purposes
@override_settings(
    FILE_UPLOAD_HANDLERS=[
        "django.core.files.uploadhandler.MemoryFileUploadHandler",
        "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    ],
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
)
class ImportActualsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.test_year = 2019
        self.test_period = 9

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
            directorate=self.directorate_obj,
            active=False,
        )
        NaturalCodeFactory.create(
            natural_account_code=self.valid_natural_account_code,
            economic_budget_code=VALID_ECONOMIC_CODE_LIST[0],
            active=False,
        )
        NaturalCodeFactory.create(
            natural_account_code=18162001,
            economic_budget_code=VALID_ECONOMIC_CODE_LIST[0],
            active=False,
        )
        NaturalCodeFactory.create(
            natural_account_code=self.not_valid_natural_account_code,
            active=False,
        )
        ProgrammeCodeFactory.create(
            programme_code=self.programme_code,
            active=False,
        )
        ProgrammeCodeFactory.create(
            programme_code='310540'
        )
        ProgrammeCodeFactory.create(
            programme_code='310530'
        )

        self.period_obj = FinancialPeriod.objects.get(
            period_calendar_code=self.test_period
        )
        self.year_obj = FinancialYear.objects.get(financial_year=2019)
        dummy_upload = FileUpload(
            s3_document_file='dummy.csv',
            uploading_user=self.test_user,
            document_type=FileUpload.ACTUALS,
        )
        dummy_upload.save()
        self.check_financial_code = CheckFinancialCode(dummy_upload)

    def test_save_row(self):

        self.assertEqual(
            FinancialCode.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        chart_of_account_line_correct = \
            '3000-30000-{}-{}-{}-00000-00000-0000-0000-0000'.format(
                self.cost_centre_code,
                self.valid_natural_account_code,
                self.programme_code
            )
        self.assertEqual(
            CostCentre.objects.get(cost_centre_code=self.cost_centre_code).active,
            False
        )
        self.assertEqual(
            NaturalCode.objects.get(
                natural_account_code=self.valid_natural_account_code
            ).active,
            False
        )
        self.assertEqual(
            ProgrammeCode.objects.get(programme_code=self.programme_code).active,
            False
        )

        save_trial_balance_row(
            chart_of_account_line_correct,
            self.test_amount,
            self.period_obj,
            self.year_obj,
            self.check_financial_code,
            2
        )
        self.assertEqual(
            CostCentre.objects.get(cost_centre_code=self.cost_centre_code).active,
            True
        )
        self.assertEqual(
            NaturalCode.objects.get(
                natural_account_code=self.valid_natural_account_code
            ).active,
            True
        )
        self.assertEqual(
            ProgrammeCode.objects.get(programme_code=self.programme_code).active,
            True
        )

        self.assertEqual(
            FinancialCode.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            1
        )
        q = ActualUploadMonthlyFigure.objects.get(
            financial_code__cost_centre=self.cost_centre_code,
        )

        self.assertEqual(
            q.amount,
            self.test_amount * 100,
        )
        save_trial_balance_row(
            chart_of_account_line_correct,
            self.test_amount * 2,
            self.period_obj,
            self.year_obj,
            self.check_financial_code,
            1
        )
        # check that lines with the same chart of account are added together
        self.assertEqual(
            ActualUploadMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            1,
        )
        q = ActualUploadMonthlyFigure.objects.get(
            financial_code__cost_centre=self.cost_centre_code,
        )
        self.assertEqual(
            q.amount,
            self.test_amount * 100 * 3,
        )

    def test_save_row_no_programme(self):
        self.assertEqual(
            ActualUploadMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code).count(),
            0,
        )
        chart_of_account_line_no_programme = \
            '3000-30000-{}-{}-000000-00000-00000-0000-0000-0000'.format(
                self.cost_centre_code,
                self.valid_natural_account_code,
            )

        save_trial_balance_row(
            chart_of_account_line_no_programme,
            0,
            self.period_obj,
            self.year_obj,
            self.check_financial_code,
            2
        )
        # Lines with 0 programme and 0 amount are not saved
        self.assertEqual(
            ActualUploadMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code).count(),
            0,
        )
        #   Now save a valid value
        save_trial_balance_row(
            chart_of_account_line_no_programme,
            self.test_amount,
            self.period_obj,
            self.year_obj,
            self.check_financial_code,
            3
        )

        q = FinancialCode.objects.get(
            cost_centre=self.cost_centre_code
        )
        self.assertEqual(
            int(q.programme.programme_code),
            GENERIC_PROGRAMME_CODE
        )
        self.assertEqual(
            ActualUploadMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code).count(),
            1,
        )

    def test_save_row_invalid_nac(self):
        self.assertEqual(
            FinancialCode.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        self.assertEqual(
            NaturalCode.objects.get(
                natural_account_code=self.not_valid_natural_account_code
            ).active,
            False
        )
        self.assertEqual(
            CostCentre.objects.get(cost_centre_code=self.cost_centre_code).active,
            False
        )
        self.assertEqual(
            ProgrammeCode.objects.get(programme_code=self.programme_code).active,
            False
        )

        save_trial_balance_row(
            '3000-30000-{}-{}-{}-00000-00000-0000-0000-0000'.format(
                self.cost_centre_code,
                self.not_valid_natural_account_code,
                self.programme_code
            ),
            10,
            self.period_obj,
            self.year_obj,
            self.check_financial_code,
            1
        )
        # The chart of account fields are still non active
        # because the row was ignored
        self.assertEqual(
            NaturalCode.objects.get(
                natural_account_code=self.not_valid_natural_account_code
            ).active,
            False
        )
        self.assertEqual(
            CostCentre.objects.get(cost_centre_code=self.cost_centre_code).active,
            False
        )
        self.assertEqual(
            ProgrammeCode.objects.get(programme_code=self.programme_code).active,
            False
        )
        self.assertEqual(
            FinancialCode.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        self.assertEqual(
            self.check_financial_code.error_found,
            False,
        )

        save_trial_balance_row(
            '3000-30000-123456-12345678-123456-12345-12345-1234-1234-1234',
            10,
            self.period_obj,
            self.year_obj,
            self.check_financial_code,
            2
        )
        self.assertEqual(
            self.check_financial_code.error_found,
            True,
        )

    def test_upload_trial_balance_report(self):
        # Check that BadZipFile is raised on
        # supply of incorrect file format
        bad_file_type_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/bad_file_type.csv',
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.ACTUALS,
        )
        bad_file_type_upload.save()
        with self.assertRaises(BadZipFile):
            upload_trial_balance_report(
                bad_file_type_upload,
                self.test_period,
                self.test_year,
            )

        bad_title_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/bad_title_upload_test.xlsx',
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.ACTUALS,
        )
        bad_title_file_upload.save()

        with self.assertRaises(UploadFileFormatError):
            upload_trial_balance_report(
                bad_title_file_upload,
                self.test_period,
                self.test_year,
            )

        self.assertEqual(
            FinancialCode.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        cost_centre_code_1 = 888888
        CostCentreFactory.create(
            cost_centre_code=cost_centre_code_1,
            directorate=self.directorate_obj
        )
        # Prepare to upload data. Create some data that will be deleted
        save_trial_balance_row(
            '3000-30000-{}-{}-{}-00000-00000-0000-0000-0000'.format(
                cost_centre_code_1,
                self.valid_natural_account_code,
                self.programme_code
            ),
            self.test_amount,
            self.period_obj,
            self.year_obj,
            self.check_financial_code,
            2
        )

        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=cost_centre_code_1,
            ).count(),
            0,
        )

        self.assertEqual(
            ActualUploadMonthlyFigure.objects.filter(
                financial_code__cost_centre=cost_centre_code_1,
            ).count(),
            1,
        )

        copy_actuals_to_monthly_figure(self.period_obj, self.test_year)
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=cost_centre_code_1,
            ).count(),
            1,
        )

        self.assertEqual(
            ActualUploadMonthlyFigure.objects.filter(
                financial_code__cost_centre=cost_centre_code_1,
            ).count(),
            0,
        )

        self.assertFalse(
            FinancialPeriod.objects.get(
                period_calendar_code=self.test_period
            ).actual_loaded
        )
        bad_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/upload_bad_data.xlsx',
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.ACTUALS,
        )
        bad_file_upload.save()

        upload_trial_balance_report(
            bad_file_upload,
            self.test_period,
            self.test_year,
        )

        self.assertFalse(
            FinancialPeriod.objects.get(
                period_calendar_code=self.test_period,
            ).actual_loaded
        )

        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=cost_centre_code_1
            ).count(),
            1,
        )

        good_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/upload_test.xlsx',
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.ACTUALS,
        )
        good_file_upload.save()

        upload_trial_balance_report(
            good_file_upload,
            self.test_period,
            self.test_year,
        )
        # Check that existing figures for the same period have been deleted
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=cost_centre_code_1
            ).count(),
            0,
        )
        # Check for existence of monthly figures
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code
            ).count(),
            4,
        )
        result = ForecastMonthlyFigure.objects.filter(
            financial_code__cost_centre=self.cost_centre_code
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

    def test_check_trial_balance_format(self):
        fake_work_sheet = FakeWorkSheet()
        fake_work_sheet.title = CORRECT_TRIAL_BALANCE_WORKSHEET_NAME
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TRIAL_BALANCE_TITLE)
        fake_work_sheet[MONTH_CELL] = FakeCell(datetime(2019, 8, 1))
        # wrong month
        with self.assertRaises(UploadFileFormatError):
            check_trial_balance_format(
                fake_work_sheet,
                9,
                2019,
            )
        #   wrong year
        with self.assertRaises(UploadFileFormatError):
            check_trial_balance_format(
                fake_work_sheet,
                8,
                2018,
            )
        # Wrong title
        fake_work_sheet[TITLE_CELL] = FakeCell('Wrong Title')
        with self.assertRaises(UploadFileFormatError):
            check_trial_balance_format(
                fake_work_sheet,
                8,
                2019,
            )

    def test_check_trial_balance_format_jan(self):
        # The year on the trial balance is the calendar year,
        # and the upload year is the financial year
        # They don't match in Jan, Feb, March
        upload_month = 1
        fake_work_sheet = FakeWorkSheet()
        fake_work_sheet.title = CORRECT_TRIAL_BALANCE_WORKSHEET_NAME
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TRIAL_BALANCE_TITLE)
        fake_work_sheet[MONTH_CELL] = FakeCell(datetime(2020, upload_month, 1))
        # wrong month
        self.assertTrue(
            check_trial_balance_format(
                fake_work_sheet,
                upload_month,
                2019,
            )
        )

    def test_check_trial_balance_format_dec(self):
        upload_month = 12
        fake_work_sheet = FakeWorkSheet()
        fake_work_sheet.title = CORRECT_TRIAL_BALANCE_WORKSHEET_NAME
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TRIAL_BALANCE_TITLE)
        fake_work_sheet[MONTH_CELL] = FakeCell(datetime(2019, upload_month, 1))
        # wrong month
        self.assertTrue(
            check_trial_balance_format(
                fake_work_sheet,
                upload_month,
                2019,
            )
        )

    def test_check_trial_balance_format_feb(self):
        # The year on the trial balance is the calendar year,
        # and the upload year is the financial year
        # They don't match in Jan, Feb, March
        upload_month = 2
        fake_work_sheet = FakeWorkSheet()
        fake_work_sheet.title = CORRECT_TRIAL_BALANCE_WORKSHEET_NAME
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TRIAL_BALANCE_TITLE)
        fake_work_sheet[MONTH_CELL] = FakeCell(datetime(2020, upload_month, 1))
        # wrong month
        self.assertTrue(
            check_trial_balance_format(
                fake_work_sheet,
                upload_month,
                2019,
            )
        )

    def test_check_trial_balance_format_mar(self):
        # The year on the trial balance is the calendar year,
        # and the upload year is the financial year
        # They don't match in Jan, Feb, March
        upload_month = 3
        fake_work_sheet = FakeWorkSheet()
        fake_work_sheet.title = CORRECT_TRIAL_BALANCE_WORKSHEET_NAME
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TRIAL_BALANCE_TITLE)
        fake_work_sheet[MONTH_CELL] = FakeCell(datetime(2020, upload_month, 1))
        # wrong month
        self.assertTrue(
            check_trial_balance_format(
                fake_work_sheet,
                upload_month,
                2019,
            )
        )


# Set file upload handlers back to default as
# we need to remove S3 interactions for test purposes
@override_settings(
    FILE_UPLOAD_HANDLERS=[
        "django.core.files.uploadhandler.MemoryFileUploadHandler",
        "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    ]
)
class UploadActualsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.financial_period_code = 1
        self.financial_year_id = 2019

        self.file_mock = MagicMock(spec=File)
        self.file_mock.name = 'test.txt'

    @override_settings(ASYNC_FILE_UPLOAD=False)
    @patch('forecast.views.upload_file.process_uploaded_file')
    def test_upload_actuals_view(self, mock_process_uploaded_file):
        assert not self.test_user.has_perm("forecast.can_view_forecasts")

        uploaded_actuals_url = reverse(
            "upload_actuals_file",
        )

        # Should have been redirected (no permission)
        resp = self.client.get(
            uploaded_actuals_url,
            follow=False,
        )

        assert resp.status_code == 403

        can_upload_files = Permission.objects.get(
            codename='can_upload_files'
        )
        self.test_user.user_permissions.add(can_upload_files)
        self.test_user.save()

        resp = self.client.get(
            uploaded_actuals_url,
        )

        # Should have been permission now
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            uploaded_actuals_url,
            data={
                "period": self.financial_period_code,
                "year": self.financial_year_id,
                'file': self.file_mock,
            },
        )

        # Make sure upload was process was kicked off
        assert mock_process_uploaded_file.called

        # Should have been redirected to document upload  page
        self.assertEqual(resp.status_code, 302)
        assert resp.url == '/upload/files/'

        # Clean up file
        file_path = 'uploaded/actuals/{}'.format(
            self.file_mock.name
        )
        if os.path.exists(file_path):
            os.remove(file_path)

    @override_settings(ASYNC_FILE_UPLOAD=False)
    @patch('forecast.views.upload_file.process_uploaded_file')
    def test_finance_admin_can_upload_actuals(self, mock_process_uploaded_file):
        assert not self.test_user.groups.filter(
            name="Finance Administrator"
        )

        uploaded_actuals_url = reverse("upload_actuals_file")

        # Should have been redirected (no permission)
        resp = self.client.get(
            uploaded_actuals_url,
            follow=False,
        )

        assert resp.status_code == 403

        finance_admins = Group.objects.get(
            name='Finance Administrator',
        )
        finance_admins.user_set.add(self.test_user)
        finance_admins.save()

        resp = self.client.get(uploaded_actuals_url)

        # Should have been permission now
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            uploaded_actuals_url,
            data={
                "period": self.financial_period_code,
                "year": self.financial_year_id,
                'file': self.file_mock,
            },
        )

        # Make sure upload was process was kicked off
        assert mock_process_uploaded_file.called

        # Should have been redirected to document upload  page
        self.assertEqual(resp.status_code, 302)
        assert resp.url == '/upload/files/'

        # Clean up file
        file_path = 'uploaded/actuals/{}'.format(
            self.file_mock.name
        )
        if os.path.exists(file_path):
            os.remove(file_path)
