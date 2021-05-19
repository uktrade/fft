from django.db.models import Sum

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import BaseTestCase
from core.utils.generic_helpers import make_financial_year_current

from costcentre.test.factories import (
    CostCentreFactory,
    DirectorateFactory,
)

from forecast.import_actuals import (
    copy_current_year_actuals_to_monthly_figure,
    save_trial_balance_row,
)
from forecast.models import (
    ActualUploadMonthlyFigure,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.utils.import_helpers import (
    CheckFinancialCode,
    VALID_ECONOMIC_CODE_LIST,
)

from split_project.utils import create_split_data

from upload_file.models import FileUpload


class SplitImportActualsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.test_year = 2019
        make_financial_year_current(self.test_year)
        self.test_period = 9

        self.cost_centre_code = 109189
        self.natural_account_code = 52191003
        self.programme_code = "310940"
        self.project_code1 = 12341
        self.project_code2 = 12342
        self.project_code3 = 12343

        self.test_amount = 100
        self.directorate_obj = DirectorateFactory.create(directorate_code="T123")
        CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code,
            directorate=self.directorate_obj,
            active=False,
        )
        NaturalCodeFactory.create(
            natural_account_code=self.natural_account_code,
            economic_budget_code=VALID_ECONOMIC_CODE_LIST[0],
            active=False,
        )
        ProgrammeCodeFactory.create(
            programme_code=self.programme_code, active=False,
        )
        ProjectCodeFactory.create(project_code=self.project_code1)
        ProjectCodeFactory.create(project_code=self.project_code2)
        ProjectCodeFactory.create(project_code=self.project_code3)

        self.period_obj = FinancialPeriod.objects.get(
            period_calendar_code=self.test_period
        )

        create_split_data(
            self.cost_centre_code,
            self.natural_account_code,
            self.programme_code,
            self.project_code1,
            1000,
            self.period_obj,
        )
        create_split_data(
            self.cost_centre_code,
            self.natural_account_code,
            self.programme_code,
            self.project_code2,
            215,
            self.period_obj,
        )
        create_split_data(
            self.cost_centre_code,
            self.natural_account_code,
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
        # Prepare to upload data - create some data that will be deleted
        save_trial_balance_row(
            "3000-30000-{}-{}-{}-00000-00000-0000-0000-0000".format(
                self.cost_centre_code, self.natural_account_code, self.programme_code
            ),
            self.test_amount,
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
        # and 3 created by splitting by project code
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code
            ).count(),
            4,
        )
        result = ForecastMonthlyFigure.objects.filter(
            financial_code__cost_centre=self.cost_centre_code
        ).aggregate(total=Sum("amount"))

        # Check that figures have correct values
        self.assertEqual(
            result["total"], self.test_amount * 100,
        )
