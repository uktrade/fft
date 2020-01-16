from unittest.mock import MagicMock

from django.core.files import File
from django.test import TestCase

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from costcentre.test.factories import CostCentreFactory

from forecast.forms import (
    AddForecastRowForm,
    UploadActualsForm,
)
from forecast.models import (
    FinancialCode,
    ForecastMonthlyFigure,
)


class TestAddForecastRowForm(TestCase):
    def setUp(self):
        self.nac_code = 999999
        self.cost_centre_code = 888812
        self.analysis_1_code = "1111111"
        self.analysis_2_code = "2222222"
        self.project_code = "3000"

        self.programme = ProgrammeCodeFactory.create()
        self.cost_centre = NaturalCodeFactory.create(
            natural_account_code=self.nac_code,
        )
        self.project = ProjectCodeFactory.create(
            project_code=self.project_code,
        )
        CostCentreFactory.create(cost_centre_code=self.cost_centre_code)
        self.analysis_1 = Analysis1Factory.create(
            analysis1_code=self.analysis_1_code,
        )
        self.analysis_2 = Analysis2Factory.create(
            analysis2_code=self.analysis_2_code,
        )

    def test_valid_data(self):
        form = AddForecastRowForm(
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac_code,
                "analysis1_code": self.analysis_1.analysis1_code,
                "analysis2_code": self.analysis_2.analysis2_code,
                "project_code": self.project_code,
            }
        )

        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = AddForecastRowForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "programme": ["This field is required."],
                "natural_account_code": ["This field is required."],
            },
        )

    def test_duplicate_row_invalid(self):
        financial_code = FinancialCode.objects.create(
            cost_centre_id=self.cost_centre_code,
            programme=self.programme,
            natural_account_code=self.cost_centre,
            analysis1_code=self.analysis_1,
            analysis2_code=self.analysis_2,
            project_code=self.project,
        )

        monthly_figure = ForecastMonthlyFigure(
            financial_year_id=2019,
            financial_period_id=1,
            financial_code=financial_code,
        )
        monthly_figure.save()

        form = AddForecastRowForm(
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac_code,
                "analysis1_code": self.analysis_1.analysis1_code,
                "analysis2_code": self.analysis_2.analysis2_code,
                "project_code": self.project_code,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "__all__": [
                    "A row already exists with these details, "
                    "please amend the values you are supplying"
                ],
            },
        )

    def test_same_values_for_programme_and_natural_account_code_valid(self):
        financial_code = FinancialCode.objects.create(
            cost_centre_id=self.cost_centre_code,
            programme=self.programme,
            natural_account_code=self.cost_centre,
            analysis1_code=self.analysis_1,
            analysis2_code=self.analysis_2,
            project_code=self.project,
        )

        monthly_figure = ForecastMonthlyFigure(
            financial_year_id=2019,
            financial_period_id=1,
            financial_code=financial_code,
        )
        monthly_figure.save()

        form = AddForecastRowForm(
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac_code,
                "analysis1_code": None,
                "analysis2_code": None,
                "project_code": None,
            }
        )

        self.assertTrue(form.is_valid())


class TestAddUploadActualsForm(TestCase):
    def setUp(self):
        self.financial_period_code = 1
        self.financial_year_id = 2019

        self.file_mock = MagicMock(spec=File)
        self.file_mock.name = 'test.txt'

    def test_valid_data(self):
        form = UploadActualsForm(
            data={
                "period": self.financial_period_code,
                "year": self.financial_year_id,
            },
            files={
                'file': self.file_mock,
            }
        )

        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = UploadActualsForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "file": ["This field is required."],
                "period": ["This field is required."],
                "year": ["This field is required."],
            },
        )
