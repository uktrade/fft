from rest_framework.reverse import reverse

from django.test import (
    TestCase,
)

from rest_framework.test import APIClient

from end_of_month.test.test_utils import (
    SetFullYearArchive,
)


class MIReportDataTests(TestCase):

    def test_forecast_data_returned_in_response(self):
        SetFullYearArchive()
        self.url_name = "data_lake_mi_report_data"
        response = self.get_data()

        assert response['Content-Type'] == 'text/csv'
        rows = response.content.decode("utf-8").split("\n")

        cols = rows[0].split(",")
        assert len(cols) == 16
        assert len(rows) == 104

    def get_data(self):
        test_url = f"http://testserver{reverse(self.url_name)}"

        return APIClient().get(
            test_url,
            content_type="",
        )
