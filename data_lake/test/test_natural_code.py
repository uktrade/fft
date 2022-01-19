from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    HistoricalExpenditureCategoryFactory,
    HistoricalNaturalCodeFactory,
    NaturalCodeFactory,
)


class NaturalCodeTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = "12345678"
        past_year = 2019
        NaturalCodeFactory.create(natural_account_code=self.current_code)
        self.archived_code = HistoricalNaturalCodeFactory.create(
            financial_year_id=past_year,
            expenditure_category=HistoricalExpenditureCategoryFactory.create(
                financial_year_id=past_year
            ),
        ).natural_account_code

        self.url_name = "data_lake_natural_code"
        self.row_lenght = 10
        self.code_position = 7
        self.check_data()


class ArchivedNaturalCodeTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = "12345678"
        past_year = 2019
        NaturalCodeFactory.create(natural_account_code=self.current_code)
        self.archived_code = HistoricalNaturalCodeFactory.create(
            financial_year_id=past_year,
            expenditure_category=HistoricalExpenditureCategoryFactory.create(
                financial_year_id=past_year,
                linked_budget_code=12345,
            ),
        ).natural_account_code

        self.url_name = "data_lake_natural_code"
        self.row_lenght = 10
        self.code_position = 7
        self.check_data()
