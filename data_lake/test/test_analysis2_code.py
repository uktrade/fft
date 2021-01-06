from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    HistoricalAnalysis2Factory,
    Analysis2Factory,
)


class Analysis2CodeTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = Analysis2Factory.create().analysis2_code
        self.archived_code = HistoricalAnalysis2Factory.create(
            financial_year_id=2019
        ).analysis2_code

        self.url_name = "data_lake_analysis2_code"
        self.row_lenght = 3
        self.code_position = 0
        self.check_data()
