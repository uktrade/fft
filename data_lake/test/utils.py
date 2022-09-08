import csv
import io

from django.test import TestCase, override_settings
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from data_lake.test.test_hawk import hawk_auth_sender


class DataLakeTesting(TestCase):
    @override_settings(
        HAWK_INCOMING_ACCESS_KEY="some-id",
        HAWK_INCOMING_SECRET_KEY="some-secret",
    )
    def get_data(self):
        test_url = f"http://testserver{reverse(self.url_name)}"

        sender = hawk_auth_sender(url=test_url)
        return APIClient().get(
            test_url,
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

    def check_data(self):
        response = self.get_data()
        assert response["Content-Type"] == "text/csv"
        content = response.content.decode("utf-8")
        data = csv.reader(io.StringIO(content))
        rows = list(data)
        assert len(rows[0]) == self.row_lenght
        current_row = rows[1]
        archive_row = rows[2]
        assert str(current_row[self.code_position]) == str(self.current_code)

        # Check the archived value
        assert str(archive_row[self.code_position]) == str(self.archived_code)
