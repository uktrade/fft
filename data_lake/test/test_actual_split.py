from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)
from core.models import FinancialYear
from core.test.test_base import TEST_COST_CENTRE
from core.utils.generic_helpers import get_current_financial_year
from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)
from data_lake.test.utils import DataLakeTesting
from forecast.models import FinancialCode, FinancialPeriod
from upload_split_file.models import SplitPayActualFigure


class ActualSplitTests(DataLakeTesting):
    def setUp(self):
        group_name = "Test Group"
        self.group_code = "TestGG"
        directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = TEST_COST_CENTRE

        group_obj = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=group_name,
        )
        directorate_obj = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=directorate_name,
            group=group_obj,
        )
        cost_centre_obj = CostCentreFactory(
            directorate=directorate_obj,
            cost_centre_code=self.cost_centre_code,
        )
        current_year = get_current_financial_year()
        programme_obj = ProgrammeCodeFactory()
        self.programme_code = programme_obj.programme_code
        nac_obj = NaturalCodeFactory(economic_budget_code="RESOURCE")
        self.nac = nac_obj.natural_account_code
        project_obj = ProjectCodeFactory()
        self.project_code = project_obj.project_code
        self.year_obj = FinancialYear.objects.get(financial_year=current_year)
        self.financial_code_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cost_centre_obj,
            natural_account_code=nac_obj,
            project_code=project_obj,
        )
        financial_period_queryset = FinancialPeriod.objects.filter(
            financial_period_code__lt=4
        )

        amount = 0
        for period_obj in financial_period_queryset:
            SplitPayActualFigure.objects.create(
                financial_period=period_obj,
                financial_year_id=current_year,
                financial_code=self.financial_code_obj,
                amount=amount,
            )
            amount += 10000

    def test_actual_split_data_returned_in_response(self):
        self.url_name = "data_lake_actual_split"
        response = self.get_data()
        assert response["Content-Type"] == "text/csv"
        rows = response.content.decode("utf-8").split("\n")
        cols = rows[0].split(",")
        assert len(cols) == 12
        assert len(rows) == 5
