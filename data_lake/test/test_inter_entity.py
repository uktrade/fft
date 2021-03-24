from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    InterEntityFactory,
    HistoricalInterEntityFactory,
)


class InterEntityTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = InterEntityFactory.create().l2_value
        self.archived_code = HistoricalInterEntityFactory.create(
            financial_year_id=2019
        ).l2_value

        self.url_name = "data_lake_inter_entity"
        self.row_lenght = 6
        self.code_position = 3
        self.check_data()
