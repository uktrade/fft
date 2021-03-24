from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    FCOMappingFactory,
    HistoricalFCOMappingFactory,
)


class FCOMappingTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = FCOMappingFactory.create().fco_code
        self.archived_code = HistoricalFCOMappingFactory.create(
            financial_year_id=2019
        ).fco_code

        self.url_name = "data_lake_fco_mapping"
        self.row_lenght = 8
        self.code_position = 5
        self.check_data()
