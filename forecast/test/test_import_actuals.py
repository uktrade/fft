import os
from datetime import datetime
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

from forecast.import_actuals import (
    CORRECT_TITLE,
    CORRECT_WS_TITLE,
    GENERIC_PROGRAMME_CODE,
    MONTH_CELL,
    TITLE_CELL,
    TrialBalanceError,
    VALID_ECONOMIC_CODE_LIST,
    check_trial_balance_format,
    copy_actuals_to_monthly_figure,
    save_tb_row,
    upload_trial_balance_report,
)
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
    UploadingActuals,
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


class ImportActualsTest(TestCase):
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

        self.test_user_email = "test@test.com"
        self.test_password = "password"
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email,
        )

        self.test_user.set_password(self.test_password)

    def test_save_row(self):
        self.assertEqual(
            UploadingActuals.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        chart_of_account_line_correct = \
            '3000-30000-{}-{}-{}-00000-00000-0000-0000-0000'.format(
                self.cost_centre_code,
                self.valid_natural_account_code,
                self.programme_code
            )

        save_tb_row(
            chart_of_account_line_correct,
            self.test_amount,
            self.period_obj,
            self.year_obj,
        )

        self.assertEqual(
            UploadingActuals.objects.filter(cost_centre=self.cost_centre_code).count(),
            1,
        )
        q = UploadingActuals.objects.get(cost_centre=self.cost_centre_code)
        self.assertEqual(
            q.amount,
            self.test_amount * 100,
        )

        save_tb_row(
            chart_of_account_line_correct,
            self.test_amount * 2,
            self.period_obj,
            self.year_obj,
        )
        # check that lines with the same chart of account are added together
        self.assertEqual(
            UploadingActuals.objects.filter(cost_centre=self.cost_centre_code).count(),
            1,
        )
        q = UploadingActuals.objects.get(cost_centre=self.cost_centre_code)
        self.assertEqual(
            q.amount,
            self.test_amount * 100 * 3,
        )

    def test_save_row_no_programme(self):
        self.assertEqual(
            UploadingActuals.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        chart_of_account_line_no_programme = \
            '3000-30000-{}-{}-000000-00000-00000-0000-0000-0000'.format(
                self.cost_centre_code,
                self.valid_natural_account_code,
            )

        save_tb_row(
            chart_of_account_line_no_programme,
            0,
            self.period_obj,
            self.year_obj,
        )
        # Lines with 0 programme and 0 amount are not saved
        self.assertEqual(
            UploadingActuals.objects.filter(cost_centre=self.cost_centre_code).count(),
            0,
        )
        save_tb_row(
            chart_of_account_line_no_programme,
            self.test_amount,
            self.period_obj,
            self.year_obj,
        )
        q = UploadingActuals.objects.get(cost_centre=self.cost_centre_code)

        self.assertEqual(
            q.amount,
            self.test_amount * 100
        )
        self.assertEqual(
            int(q.programme.programme_code),
            GENERIC_PROGRAMME_CODE
        )

    def test_save_row_invalid_nac(self):
        self.assertEqual(
            UploadingActuals.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        save_tb_row(
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
            UploadingActuals.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        with self.assertRaises(TrialBalanceError):
            save_tb_row(
                '3000-30000-123456-12345678-123456-12345-12345-1234-1234-1234'.format(
                    '123456',
                    self.not_valid_natural_account_code,
                    self.programme_code
                ),
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

        with self.assertRaises(TrialBalanceError):
            upload_trial_balance_report(
                bad_title_file_upload,
                self.test_period,
                self.test_year,
            )

        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        self.assertEqual(
            UploadingActuals.objects.filter(
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
        save_tb_row(
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
            MonthlyFigure.objects.filter(
                cost_centre=cost_centre_code_1
            ).count(),
            0,
        )

        self.assertEqual(
            UploadingActuals.objects.filter(
                cost_centre=cost_centre_code_1
            ).count(),
            1,
        )

        copy_actuals_to_monthly_figure(self.period_obj, self.test_year)
        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=cost_centre_code_1
            ).count(),
            1,
        )
        self.assertEqual(
            UploadingActuals.objects.filter(
                cost_centre=cost_centre_code_1
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

        with self.assertRaises(TrialBalanceError):
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

        upload_trial_balance_report(
            good_file_upload,
            self.test_period,
            self.test_year,
        )
        # Check that existing figures for the same period have been deleted
        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=cost_centre_code_1
            ).count(),
            0,
        )
        # Check for existence of monthly figures
        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            4,
        )
        result = MonthlyFigure.objects.filter(
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

    def test_check_trial_balance_format(self):
        fake_work_sheet = FakeWorkSheet()
        fake_work_sheet.title = CORRECT_WS_TITLE
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TITLE)
        fake_work_sheet[MONTH_CELL] = FakeCell(datetime(2019, 8, 1))
        # wrong month
        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                9,
                2019,
            )
        #   wrong year
        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                8,
                2018,
            )
        # Wrong title
        fake_work_sheet[TITLE_CELL] = FakeCell('Wrong Title')
        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                8,
                2019,
            )
        # wrong worksheet title
        fake_work_sheet.title = 'Unknown'
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TITLE)
        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                8,
                2019,
            )
