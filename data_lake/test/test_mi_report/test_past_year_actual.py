from core.utils.generic_helpers import get_current_financial_year
from data_lake.test.utils import DataLakeTesting
from end_of_month.test.test_utils import SetFullYearArchive
from previous_years.test.test_utils import PastYearForecastSetup


class PastActualTests(DataLakeTesting, PastYearForecastSetup):
    def test_data_returned_in_response(self):

        SetFullYearArchive(year=get_current_financial_year() - 1)
        self.url_name = "mi_report_previous_year_data"
        response = self.get_data()

        assert response["Content-Type"] == "text/csv"
        rows = response.content.decode("utf-8").split("\n")
        cols = rows[0].split(",")
        assert len(cols) == 16
        assert len(rows) == 14
