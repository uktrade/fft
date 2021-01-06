from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    ExpenditureCategoryFactory,
    HistoricalExpenditureCategoryFactory,
)


class ExpenditureCategoryTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = ExpenditureCategoryFactory.create().grouping_description
        self.archived_code = HistoricalExpenditureCategoryFactory.create(
            financial_year_id=2019
        ).grouping_description

        self.url_name = "data_lake_expenditure_category"
        self.row_lenght = 5
        self.code_position = 1
        self.check_data()
