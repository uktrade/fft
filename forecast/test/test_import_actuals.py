import os
from datetime import datetime
from typing import (
    Dict,
    TypeVar,
)
from unittest.mock import MagicMock, patch
from zipfile import BadZipFile

from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.db.models import Sum
from django.test import (
    RequestFactory,
    TestCase,
    override_settings,
)
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import RequestFactoryBase

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
    UploadFileDataError,
    UploadFileFormatError,
    VALID_ECONOMIC_CODE_LIST,
    check_trial_balance_format,
    copy_actuals_to_monthly_figure,
    save_trial_balance_row,
    upload_trial_balance_report,
)
from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastPermission,
    MonthlyFigure,
    MonthlyFigureAmount,
)
from forecast.test.factories import (
    ForecastPermissionFactory,
)
from forecast.views.upload_file import (
    UploadActualsView,
)

from upload_file.models import FileUpload

TEST_COST_CENTRE = 109189
TEST_VALID_NATURAL_ACCOUNT_CODE = 52191003
TEST_NOT_VALID_NATURAL_ACCOUNT_CODE = 92191003
TEST_PROGRAMME_CODE = '310940'
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class FakeWorkSheet(Dict[_KT, _VT]):
    title = None


class FakeCell:
    value = None

    def __init__(self, value):
        self.value = value


class ImportActualsTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

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
            economic_budget_code=VALID_ECONOMIC_CODE_LIST[0]
        )
        NaturalCodeFactory.create(
            natural_account_code=18162001,
            economic_budget_code=VALID_ECONOMIC_CODE_LIST[0]
        )
        NaturalCodeFactory.create(
            natural_account_code=self.not_valid_natural_account_code
        )
        ProgrammeCodeFactory.create(
            programme_code=self.programme_code
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

    def test_save_row(self):
        self.assertEqual(
            FinancialCode.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        self.assertEqual(
            MonthlyFigure.objects.filter(
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

        save_trial_balance_row(
            chart_of_account_line_correct,
            self.test_amount,
            self.period_obj,
            self.year_obj,
        )

        self.assertEqual(
            FinancialCode.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            1
        )
        q = MonthlyFigureAmount.objects.get(
            monthly_figure__financial_code__cost_centre=self.cost_centre_code,
            version=MonthlyFigureAmount.TEMPORARY_VERSION
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
        )
        # check that lines with the same chart of account are added together
        self.assertEqual(
            MonthlyFigureAmount.objects.filter(
                monthly_figure__financial_code__cost_centre=self.cost_centre_code,
                version=MonthlyFigureAmount.TEMPORARY_VERSION
            ).count(),
            1,
        )
        q = MonthlyFigureAmount.objects.get(
            monthly_figure__financial_code__cost_centre=self.cost_centre_code,
            version=MonthlyFigureAmount.TEMPORARY_VERSION
        )
        self.assertEqual(
            q.amount,
            self.test_amount * 100 * 3,
        )

    def test_save_row_no_programme(self):
        self.assertEqual(
            MonthlyFigure.objects.filter(
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
        )
        # Lines with 0 programme and 0 amount are not saved
        self.assertEqual(
            MonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code).count(),
            0,
        )
        #   Now save a valid value
        save_trial_balance_row(
            chart_of_account_line_no_programme,
            self.test_amount,
            self.period_obj,
            self.year_obj,
        )

        q = FinancialCode.objects.get(
            cost_centre=self.cost_centre_code
        )
        self.assertEqual(
            int(q.programme.programme_code),
            GENERIC_PROGRAMME_CODE
        )
        self.assertEqual(
            MonthlyFigure.objects.filter(
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
        save_trial_balance_row(
            '3000-30000-{}-{}-{}-00000-00000-0000-0000-0000'.format(
                self.cost_centre_code,
                self.not_valid_natural_account_code,
                self.programme_code
            ),
            10,
            self.period_obj,
            self.year_obj,
        )
        self.assertEqual(
            FinancialCode.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        with self.assertRaises(UploadFileDataError):
            save_trial_balance_row(
                '3000-30000-123456-12345678-123456-12345-12345-1234-1234-1234',
                10,
                self.period_obj,
                self.year_obj,
            )

    def test_upload_trial_balance_report(self):
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
            upload_trial_balance_report(
                bad_file_type_upload,
                self.test_period,
                self.test_year,
            )

        bad_title_file_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/bad_title_upload_test.xlsx',
            ),
            uploading_user=self.test_user,
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
        )

        self.assertEqual(
            MonthlyFigureAmount.objects.filter(
                monthly_figure__financial_code__cost_centre=cost_centre_code_1,
                version=MonthlyFigureAmount.CURRENT_VERSION
            ).count(),
            0,
        )

        self.assertEqual(
            MonthlyFigureAmount.objects.filter(
                monthly_figure__financial_code__cost_centre=cost_centre_code_1,
                version=MonthlyFigureAmount.TEMPORARY_VERSION
            ).count(),
            1,
        )

        copy_actuals_to_monthly_figure(self.period_obj, self.test_year)
        self.assertEqual(
            MonthlyFigureAmount.objects.filter(
                monthly_figure__financial_code__cost_centre=cost_centre_code_1,
                version=MonthlyFigureAmount.CURRENT_VERSION
            ).count(),
            1,
        )

        self.assertEqual(
            MonthlyFigureAmount.objects.filter(
                monthly_figure__financial_code__cost_centre=cost_centre_code_1,
                version=MonthlyFigureAmount.TEMPORARY_VERSION
            ).count(),
            0,
        )

        self.assertFalse(
            FinancialPeriod.objects.get(
                period_calendar_code=self.test_period
            ).actual_loaded
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
            MonthlyFigure.objects.filter(
                financial_code__cost_centre=cost_centre_code_1
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

        upload_trial_balance_report(
            good_file_upload,
            self.test_period,
            self.test_year,
        )
        # Check that existing figures for the same period have been deleted
        self.assertEqual(
            MonthlyFigureAmount.objects.filter(
                monthly_figure__financial_code__cost_centre=cost_centre_code_1
            ).count(),
            0,
        )
        # Check for existence of monthly figures
        self.assertEqual(
            MonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code
            ).count(),
            4,
        )
        result = MonthlyFigureAmount.objects.filter(
            monthly_figure__financial_code__cost_centre=self.cost_centre_code
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


class UploadActualsTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.financial_period_code = 1
        self.financial_year_id = 2019

        self.file_mock = MagicMock(spec=File)
        self.file_mock.name = 'test.txt'

    @override_settings(ASYNC_FILE_UPLOAD=False)
    @patch('forecast.views.upload_file.process_uploaded_file')
    def test_upload_actuals_view(self, mock_process_uploaded_file):
        forecast_permission_count = ForecastPermission.objects.all().count()
        self.assertEqual(forecast_permission_count, 0)

        uploaded_actuals_url = reverse(
            "upload_actuals_file",
        )

        # Should have been redirected (no permission)
        with self.assertRaises(PermissionDenied):
            self.factory_get(
                uploaded_actuals_url,
                UploadActualsView,
            )

        ForecastPermissionFactory.create(
            user=self.test_user,
            can_upload=True,
        )

        resp = self.factory_get(
            uploaded_actuals_url,
            UploadActualsView,
        )

        # Should have been permission now
        self.assertEqual(resp.status_code, 200)

        resp = self.factory_post(
            uploaded_actuals_url,
            {
                "period": self.financial_period_code,
                "year": self.financial_year_id,
                'file': self.file_mock,
            },
            UploadActualsView,
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
