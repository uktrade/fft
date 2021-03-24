from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    CommercialCategoryFactory,
    HistoricalCommercialCategoryFactory,
)


class ExpenditureCategoryTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = CommercialCategoryFactory.create().commercial_category
        self.archived_code = HistoricalCommercialCategoryFactory.create(
            financial_year_id=2019
        ).commercial_category

        self.url_name = "data_lake_commercial_category"
        self.row_lenght = 3
        self.code_position = 1
        self.check_data()
