from data_lake.test.utils import DataLakeTesting
from end_of_month.models import EndOfMonthStatus
from previous_years.test.test_utils import PastYearForecastSetup


class PastActualTests(DataLakeTesting, PastYearForecastSetup):
    def test_data_returned_in_response(self):
        max_period_id = (
            EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
        )
        assert max_period_id == 0
        for period in range(max_period_id + 1, max_period_id + 4):
            end_of_month_info = EndOfMonthStatus.objects.get(
                archived_period__financial_period_code=period
            )
            end_of_month_info.archived = True
            end_of_month_info.save()

        self.url_name = "mi_report_financial_period_in_use"
        response = self.get_data()

        assert response["Content-Type"] == "text/csv"
        rows = response.content.decode("utf-8").split("\n")
        cols = rows[0].split(",")
        assert len(cols) == 2
        # 7 rows: header, Period 0, the 4 archived period and an empty row at the end
        assert len(rows) == 7
