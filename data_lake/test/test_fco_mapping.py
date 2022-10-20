from chartofaccountDIT.test.factories import (
    FCOMappingFactory,
    HistoricalFCOMappingFactory,
)
from data_lake.test.utils import DataLakeTesting


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

    def test_data_returned_in_response_no_nac(self):
        fco_obj = FCOMappingFactory.create()
        self.current_code = fco_obj.fco_code
        fco_obj.account_L6_code_fk = None
        fco_obj.save()
        self.archived_code = HistoricalFCOMappingFactory.create(
            financial_year_id=2019
        ).fco_code

        self.url_name = "data_lake_fco_mapping"
        self.row_lenght = 8
        self.code_position = 5
        self.check_data()
