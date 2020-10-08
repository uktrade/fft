from data_lake.tests.test_hawk import (
    hawk_auth_sender,
    test_url,
)

from django.test import (
    TestCase,
    override_settings,
)

from rest_framework.test import APIClient


class ForecastTests(TestCase):
    @override_settings(
        HAWK_INCOMING_ACCESS_KEY="some-id",
        HAWK_INCOMING_SECRET_KEY="some-secret",
    )
    def test_forecast_data_returned_in_response(self):
        sender = hawk_auth_sender()
        response = APIClient().get(
            test_url,
            content_type='',
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
        )

        assert response['Content-Type'] == 'text/csv'
        rows = response.content.decode("utf-8").split("\n")

        cols = rows[0].split(",")
        assert len(cols) == 42
