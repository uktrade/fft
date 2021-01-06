import datetime

from django.test import (
    TestCase,
    override_settings,
)

from freezegun import freeze_time

import mohawk

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


test_url = 'http://testserver' + reverse('data_lake_forecast')


def hawk_auth_sender(
    key_id='some-id',
    secret_key='some-secret',
    url=test_url,
    method='GET',
    content='',
    content_type='',
):
    credentials = {
        'id': key_id,
        'key': secret_key,
        'algorithm': 'sha256',
    }
    return mohawk.Sender(
        credentials,
        url,
        method,
        content=content,
        content_type=content_type,
    )


class HawkTests(TestCase):
    @override_settings(
        HAWK_INCOMING_ACCESS_KEY="some-id",
        HAWK_INCOMING_SECRET_KEY="some-secret",
    )
    def test_empty_object_returned_with_authentication(self):
        """If the Authorization and X-Forwarded-For headers are correct, then
        the correct, and authentic, data is returned
        """
        sender = hawk_auth_sender()
        response = APIClient().get(
            test_url,
            content_type='',
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
        )

        assert response.status_code == status.HTTP_200_OK

    @override_settings(
        HAWK_INCOMING_ACCESS_KEY="wrong-id",
        HAWK_INCOMING_SECRET_KEY="some-secret",
    )
    def test_bad_credentials_mean_401_returned(self):
        """If the wrong credentials are used,
        then a 401 is returned
        """
        sender = hawk_auth_sender()
        response = APIClient().get(
            test_url,
            content_type='',
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error = {'detail': 'Incorrect authentication credentials.'}
        assert response.json() == error

    @override_settings(
        HAWK_INCOMING_ACCESS_KEY="some-id",
        HAWK_INCOMING_SECRET_KEY="some-secret",
    )
    def test_if_61_seconds_in_past_401_returned(self):
        """If the Authorization header is generated 61 seconds in the past, then a
        401 is returned
        """
        past = datetime.datetime.now() - datetime.timedelta(seconds=61)
        with freeze_time(past):
            auth = hawk_auth_sender().request_header
        response = APIClient().get(
            reverse('data_lake_forecast'),
            content_type='',
            HTTP_AUTHORIZATION=auth,
            HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error = {'detail': 'Incorrect authentication credentials.'}
        assert response.json() == error
