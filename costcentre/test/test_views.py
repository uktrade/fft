import unittest

from django.test import Client
from django.urls import reverse

import pytest


@pytest.mark.django_db
class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get(reverse('costcentrefilter'))
        # if redirecting, check that we are sending to a login page
        if response.status_code == 302:
            self.assertIn('login', response.url)
        else:
            self.assertEqual(response.status_code, 200)
