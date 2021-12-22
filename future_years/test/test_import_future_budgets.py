import os
from unittest.mock import MagicMock, patch
from zipfile import BadZipFile

from django.contrib.auth.models import (
    Group,
)
from django.core.files import File
from django.db.models import Max

from django.test import (
    override_settings,
)
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import BaseTestCase

from costcentre.test.factories import (
    CostCentreFactory,
    DirectorateFactory,
)

from forecast.import_budgets import upload_budget_from_file
from forecast.models import (
    BudgetMonthlyFigure,
    FinancialPeriod,
)
from forecast.utils.import_helpers import (
    UploadFileFormatError,
)

# .all().aggregate(Max('price'))

from upload_file.models import FileUpload
from core.utils.generic_helpers import (
    get_current_financial_year,
)


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
    ],
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
)

def non_existing_future_year():
    return FinancialYear.objects.all() \
        .aggregate(Max('financial_year'))["financial_year__max"] + 1


class ImportBudgetsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.current_year = get_current_financial_year()
        self.future_year = non_existing_future_year()
        self.cost_centre_code = TEST_COST_CENTRE
        self.cost_centre_code_1 = 888888
        self.valid_natural_account_code = TEST_VALID_NATURAL_ACCOUNT_CODE
        self.not_valid_natural_account_code = TEST_NOT_VALID_NATURAL_ACCOUNT_CODE
        self.programme_code = TEST_PROGRAMME_CODE

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

        self.year_obj, _ = FinancialYear.objects.get_or_create(financial_year=2019)
        self.year_obj.current = True
        self.year_obj.save()


    def test_upload_budget_report(self):

        good_file_upload = FileUpload(
            s3_document_file=os.path.join(
                os.path.dirname(__file__), "test_assets/budget_upload_test.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        good_file_upload.save()

        # Check that the future year does not exist
        assert(
                FinancialYear.objects.filter(financial_year=self.future_year).count()
                == 0
        )
        upload_budget_from_file(
            good_file_upload, self.future_year,
        )
        # Check that the future year  exists
        assert(
                FinancialYear.objects.filter(financial_year=self.future_year).count()
                == 1
        )

        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.future_year).count(),
            24,
        )
        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.future_year,
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            12,
        )
        # Check that figures for same budgets are added together
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.future_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=1,
            )
            .first()
            .amount,
            1100,
        )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.future_year,
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
                os.path.dirname(__file__), "test_assets/budget_upload_test.xlsx",
            ),
            uploading_user=self.test_user,
            document_type=FileUpload.BUDGET,
        )
        good_file_upload.save()

        upload_budget_from_file(
            good_file_upload, self.future_year,
        )

        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(financial_year=self.future_year).count(),
            16,
        )
        # # Check that existing figures for the same period have been deleted
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.future_year,
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            8,
        )
        # Check that there are no entry for the actual periods
        for period in range(1, actual_month + 1):
            self.assertEqual(
                BudgetMonthlyFigure.objects.filter(
                    financial_year=self.future_year,
                    financial_code__cost_centre=self.cost_centre_code,
                    financial_period=period,
                ).first(),
                None,
            )
        self.assertEqual(
            BudgetMonthlyFigure.objects.filter(
                financial_year=self.future_year,
                financial_code__cost_centre=self.cost_centre_code,
                financial_period=12,
            )
            .first()
            .amount,
            2200,
        )
