from data_lake.test.utils import DataLakeTesting

from end_of_month.test.test_utils import (
    SetFullYearArchive,
)


class ForecastTests(DataLakeTesting):
    def test_forecast_data_returned_in_response(self):
        SetFullYearArchive()
        self.url_name = "data_lake_budget_forecast"
        response = self.get_data()

        assert response['Content-Type'] == 'text/csv'
        rows = response.content.decode("utf-8").split("\n")

        cols = rows[0].split(",")
        assert len(cols) == 14
        assert len(rows) == 131
