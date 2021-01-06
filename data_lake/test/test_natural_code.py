from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    HistoricalNaturalCodeFactory,
    NaturalCodeFactory,
)


class NaturalCodeTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = "12345678"
        NaturalCodeFactory.create(natural_account_code=self.current_code)
        self.archived_code = HistoricalNaturalCodeFactory.create(
            financial_year_id=2019
        ).natural_account_code

        self.url_name = "data_lake_natural_code"
        self.row_lenght = 9
        self.code_position = 6
        self.check_data()
