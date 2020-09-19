from io import StringIO

from django.test import TestCase

from core.test.test_base import RequestFactoryBase

from end_of_month.test.test_utils import SetFullYearArchive
from end_of_month.upload_archived_month import (
    WrongArchivePeriodException,
    import_single_archived_period,
)

from forecast.import_csv import WrongChartOFAccountCodeException
from forecast.models import (
    FinancialCode,
    ForecastMonthlyFigure,
)


class UploadSingleMonthTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        # Archive April, May and June
        self.init_data = SetFullYearArchive(3)

    def test_correct_upload(self):
        fin_code_obj = FinancialCode.objects.get(
            programme=self.init_data.programme_code,
            cost_centre=self.init_data.cost_centre_code,
            natural_account_code=self.init_data.nac,
            analysis1_code=None,
            analysis2_code=None,
            project_code=self.init_data.project_code,
        )

        original_amount = ForecastMonthlyFigure.objects.get(
            financial_code=fin_code_obj, financial_period_id=4, archived_status_id=2,
        ).amount
        new_amount = 800000
        in_mem_csv = StringIO(
            "cost centre,programme,natural account,analysis,analysis2,project,Jul\n"
            f"{self.init_data.cost_centre_code},"
            f"{self.init_data.programme_code},"
            f"{self.init_data.nac},0,0,"
            f"{self.init_data.project_code},"
            f"{new_amount}\n"
        )
        import_single_archived_period(in_mem_csv, 4, 2, 2020)
        new_amount_in_db = ForecastMonthlyFigure.objects.get(
            financial_code=fin_code_obj, financial_period_id=4, archived_status_id=2,
        ).amount

        self.assertEqual(new_amount * 100, new_amount_in_db)
        self.assertNotEqual(new_amount_in_db, original_amount)

    def test_archive_period_errors(self):
        in_mem_csv = StringIO(
            "cost centre,programme,natural account,analysis,analysis2,project,Jul\n"
            f"{self.init_data.cost_centre_code},"
            f"{self.init_data.programme_code},"
            f"{self.init_data.nac},0,0,"
            f"{self.init_data.project_code},"
            f"80000\n"
        )
        with self.assertRaises(WrongArchivePeriodException):
            import_single_archived_period(in_mem_csv, 2, 3, 2020)

        with self.assertRaises(WrongArchivePeriodException):
            import_single_archived_period(in_mem_csv, 10, 7, 2020)

    def test_chart_of_account_error(self):
        in_mem_csv = StringIO(
            "cost centre,programme,natural account,analysis,analysis2,project,Jul\n"
            "1,3,4,5,6,7,8\n"
        )
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_single_archived_period(in_mem_csv, 4, 2, 2020)
