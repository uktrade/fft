from django.test import TestCase

from chartofaccountDIT.test.factories import (
    ProgrammeCodeFactory,
    NaturalCodeFactory,
    Analysis1Factory,
    Analysis2Factory,
    ProjectCodeFactory,
)

from costcentre.test.factories import CostCentreFactory

from forecast.forms import AddForecastRowForm


class TestAddForecastRowForm(TestCase):
    def test_valid_data(self):
        # Set up test objects
        nac_code = 999999
        cost_centre_code = 888812
        analysis_1_code = "1111111"
        analysis_2_code = "2222222"
        project_code = "3000"

        programme = ProgrammeCodeFactory.create()
        NaturalCodeFactory.create(natural_account_code=nac_code)
        ProjectCodeFactory.create(project_code=project_code)
        CostCentreFactory.create(cost_centre_code=cost_centre_code)
        analysis_1 = Analysis1Factory.create(analysis1_code=analysis_1_code)
        analysis_2 = Analysis2Factory.create(analysis2_code=analysis_2_code)

        form = AddForecastRowForm(
            {
                "programme": programme.programme_code,
                "natural_account_code": nac_code,
                "analysis1_code": analysis_1.analysis1_code,
                "analysis2_code": analysis_2.analysis2_code,
                "project_code": project_code,
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
