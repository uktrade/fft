from core.models import FinancialYear

from forecast.import_actuals import save_trial_balance_row

from forecast.models import FinancialPeriod

from previous_years.import_actuals import copy_previous_year_actuals_to_monthly_figure
from previous_years.models import (
    ArchivedActualUploadMonthlyFigure,
    ArchivedForecastData,
)
from previous_years.utils import CheckArchivedFinancialCode
from previous_years.test.test_utils import PastYearForecastSetup

from upload_file.models import FileUpload


class ImportPastYearActualTest(PastYearForecastSetup):
    def setUp(self):
        super().setUp()
        dummy_upload = FileUpload(
            s3_document_file="dummy.csv",
            uploading_user=self.test_user,
            document_type=FileUpload.ACTUALS,
        )
        dummy_upload.save()
        self.check_financial_code = CheckArchivedFinancialCode(
            self.archived_year, dummy_upload
        )
        self.year_obj = FinancialYear.objects.get(financial_year=self.archived_year)
        self.year_obj.current = False
        self.year_obj.save()
        self.chart_of_account_line_correct = (
            f"3000-30000-"
            f"{self.cost_centre_code}-"
            f"{self.natural_account_code}-"
            f"{self.programme_code}-"
            f"{self.analisys1}-"
            f"{self.analisys2}-"
            f"{self.project_code}-"
            f"0000-"
            f"0000-0000"
        )

    def import_period(self, period_code):
        period_obj = FinancialPeriod.objects.get(financial_period_code=period_code)
        period_name = period_obj.period_short_name.lower()

        self.assertEqual(
            ArchivedActualUploadMonthlyFigure.objects.all().count(), 0,
        )
        self.assertEqual(
            ArchivedForecastData.objects.all().count(), 1,
        )
        data_obj = ArchivedForecastData.objects.all().first()
        new_value_in_pence = 23456700
        self.assertNotEqual(
            getattr(data_obj, period_name), new_value_in_pence,
        )
        save_trial_balance_row(
            self.chart_of_account_line_correct,
            new_value_in_pence / 100,
            period_obj,
            self.year_obj,
            self.check_financial_code,
            2,
            ArchivedActualUploadMonthlyFigure,
        )
        # Check that there is a row in the temporary table
        self.assertEqual(
            ArchivedActualUploadMonthlyFigure.objects.all().count(), 1,
        )
        copy_previous_year_actuals_to_monthly_figure(period_obj, self.archived_year)
        self.assertEqual(
            ArchivedForecastData.objects.all().count(), 1,
        )
        data_obj = ArchivedForecastData.objects.all().first()
        # Check that the field has been updated with the new value
        self.assertEqual(
            getattr(data_obj, period_name), new_value_in_pence,
        )
        # and the temporary table has been cleared
        self.assertEqual(
            ArchivedActualUploadMonthlyFigure.objects.all().count(), 0,
        )

    def test_import_apr(self):
        self.import_period(1)

    def test_import_may(self):
        self.import_period(2)

    def test_import_jun(self):
        self.import_period(3)

    def test_import_jul(self):
        self.import_period(4)

    def test_import_aug(self):
        self.import_period(5)

    def test_import_sep(self):
        self.import_period(6)

    def test_import_oct(self):
        self.import_period(7)

    def test_import_nov(self):
        self.import_period(8)

    def test_import_dec(self):
        self.import_period(9)

    def test_import_jan(self):
        self.import_period(10)

    def test_import_feb(self):
        self.import_period(11)

    def test_import_mar(self):
        self.import_period(12)

    def test_import_adj1(self):
        self.import_period(13)

    def test_import_adj2(self):
        self.import_period(14)

    def test_import_adj3(self):
        self.import_period(15)
