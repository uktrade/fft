from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    HistoricalProjectCodeFactory,
    ProjectCodeFactory,
)


class ProjectCodeTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = "4000"
        ProjectCodeFactory.create(project_code=self.current_code)
        self.archived_code = HistoricalProjectCodeFactory.create(
            financial_year_id=2019
        ).project_code

        self.url_name = "data_lake_project_code"
        self.row_lenght = 3
        self.code_position = 0
        self.check_data()
