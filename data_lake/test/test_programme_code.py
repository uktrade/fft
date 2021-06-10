from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    HistoricalProgrammeCodeFactory,
    ProgrammeCodeFactory,
)

from chartofaccountDIT.models import ProgrammeCode


class ProgrammeCodeTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = "123456"
        ProgrammeCodeFactory.create(programme_code=self.current_code)
        self.archived_code = HistoricalProgrammeCodeFactory.create(
            financial_year_id=2019
        ).programme_code

        self.url_name = "data_lake_programme_code"

        self.row_lenght = 4
        self.code_position = 0
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

        self.row_lenght = 4
        self.code_position = 0
        self.check_data()
