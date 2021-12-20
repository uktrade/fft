
from data_lake.test.utils import DataLakeTesting

from end_of_month.test.test_utils import (
    SetFullYearArchive,
)
from forecast.models import FinancialPeriod

from previous_years.test.test_utils import PastYearForecastSetup


class ActualTests(DataLakeTesting, PastYearForecastSetup):

    def test_actual_data_returned_in_response(self):
        SetFullYearArchive()
        obj = FinancialPeriod.objects.get(financial_period_code=4)
        obj.actual_loaded = True
        obj.save()
        self.url_name = "data_lake_actual"
        response = self.get_data()
        assert response['Content-Type'] == 'text/csv'
        rows = response.content.decode("utf-8").split("\n")
        cols = rows[0].split(",")
        assert len(cols) == 12
        assert len(rows) == 21
