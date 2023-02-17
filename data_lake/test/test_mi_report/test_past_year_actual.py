from data_lake.test.utils import DataLakeTesting
from previous_years.test.test_utils import PastYearForecastSetup


class PastActualTests(DataLakeTesting, PastYearForecastSetup):
    def test_data_returned_in_response(self):

        self.url_name = "mi_report_previous_year_data"
        response = self.get_data()

        assert response["Content-Type"] == "text/csv"
        rows = response.content.decode("utf-8").split("\n")
        cols = rows[0].split(",")
        assert len(cols) == 16
        assert len(rows) == 14
