from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    HistoricalProgrammeCodeFactory,
    ProgrammeCodeFactory,
)


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
