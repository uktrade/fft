from data_lake.test.utils import DataLakeTesting

class PastActualTests(DataLakeTesting):
    def test_data_returned_in_response(self):

        self.url_name = "mi_report_financial_period"
        response = self.get_data()

        assert response["Content-Type"] == "text/csv"
        rows = response.content.decode("utf-8").split("\n")
        cols = rows[0].split(",")
        assert len(cols) == 2
        assert len(rows) == 14
