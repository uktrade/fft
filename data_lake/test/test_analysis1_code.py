from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    HistoricalAnalysis1Factory,
    Analysis1Factory,
)


class Analysis1CodeTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = Analysis1Factory.create().analysis1_code
        self.archived_code = HistoricalAnalysis1Factory.create(
            financial_year_id=2019
        ).analysis1_code

        self.url_name = "data_lake_analysis1_code"
        self.row_lenght = 5
        self.code_position = 0
        self.check_data()
