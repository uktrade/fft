from chartofaccountDIT.models import ProgrammeCode
from chartofaccountDIT.test.factories import (
    HistoricalProgrammeCodeFactory,
    ProgrammeCodeFactory,
)
from data_lake.test.utils import DataLakeTesting


class ProgrammeCodeTests(DataLakeTesting):
    row_lenght = 5
    code_position = 0

    def test_data_returned_in_response(self):
        self.current_code = "123456"
        ProgrammeCodeFactory.create(programme_code=self.current_code)
        self.archived_code = HistoricalProgrammeCodeFactory.create(
            financial_year_id=2019
        ).programme_code

        self.url_name = "data_lake_programme_code"
        self.check_data()

    def test_programme_no_budget_code(self):
        self.current_code = "643210"
        obj = ProgrammeCode.objects.create(programme_code=self.current_code)
        obj.active = True
        obj.save()

        self.archived_code = HistoricalProgrammeCodeFactory.create(
            financial_year_id=2019
        ).programme_code
        self.url_name = "data_lake_programme_code"
        self.check_data()
