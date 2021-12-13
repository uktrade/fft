from django.db.models import Sum

from core.models import FinancialYear
from forecast.import_actuals import (
    copy_current_year_actuals_to_monthly_figure,
    save_trial_balance_row,
)
from forecast.models import (
    ActualUploadMonthlyFigure,
    ForecastMonthlyFigure,
)
from forecast.utils.import_helpers import CheckFinancialCode

from upload_split_file.test.test_utils import (
    SplitDataSetup,
    create_split_data,
)
from upload_file.models import FileUpload


class SplitImportActualsTest(SplitDataSetup):
    def setUp(self):
        super().setUp()

        create_split_data(
            self.cost_centre_code1,
            self.natural_account_code_pay1,
            self.programme_code,
            self.project_code1,
            6785,
            self.period_obj,
        )
        create_split_data(
            self.cost_centre_code,
            self.natural_account_code_pay2,
            self.programme_code,
            self.project_code2,
            215,
            self.period_obj,
        )
        create_split_data(
            self.cost_centre_code,
            self.natural_account_code_pay,
            self.programme_code,
            self.project_code3,
            3000,
            self.period_obj,
        )

        self.year_obj = FinancialYear.objects.get(financial_year=2019)
        dummy_upload = FileUpload(
            s3_document_file="dummy.csv",
            uploading_user=self.test_user,
            document_type=FileUpload.ACTUALS,
        )
        dummy_upload.save()
        self.check_financial_code = CheckFinancialCode(dummy_upload)

    def test_upload_trial_balance_report(self):
        test_amount = 100

        save_trial_balance_row(
            f"3000-30000-"
            f"{self.cost_centre_code}-"
            f"{self.natural_account_code_pay}-"
            f"{self.programme_code}-00000-00000-0000-0000-0000",
            test_amount,
            self.period_obj,
            self.year_obj,
            self.check_financial_code,
            2,
        )

        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            0,
        )

        self.assertEqual(
            ActualUploadMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            1,
        )

        copy_current_year_actuals_to_monthly_figure(self.period_obj, self.test_year)

        self.assertEqual(
            ActualUploadMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            0,
        )

        # Check for existence of monthly figures: 1 uploaded from file,
        # and 2 created by splitting by project code
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code
            ).count(),
            3,
        )
        result = ForecastMonthlyFigure.objects.filter(
            financial_code__cost_centre__directorate__directorate_code=self.directorate_code  # noqa: E501
        ).aggregate(total=Sum("amount"))

        # Check that figures have correct values
        self.assertEqual(
            result["total"], test_amount * 100,
        )
