from data_lake.test.utils import DataLakeTesting
from end_of_month.test.test_utils import SetFullYearArchive


class Forecast1Tests(DataLakeTesting):
    def test_forecast_data_returned_in_response(self):
        SetFullYearArchive()
        self.url_name = "mi_report_forecast_data_1"
        response = self.get_data()

        assert response["Content-Type"] == "text/csv"
        rows = response.content.decode("utf-8").split("\n")

        cols = rows[0].split(",")
        assert len(cols) == 17
        assert len(rows) == 74


class Forecast2Tests(DataLakeTesting):
    def test_forecast_data_returned_in_response(self):
        SetFullYearArchive()
        self.url_name = "mi_report_forecast_data_2"
        response = self.get_data()

        assert response["Content-Type"] == "text/csv"
        rows = response.content.decode("utf-8").split("\n")

        cols = rows[0].split(",")
        assert len(cols) == 17
        assert len(rows) == 98
