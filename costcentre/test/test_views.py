# from django.test import RequestFactory
#
# #https://matthewdaly.co.uk/blog/2015/08/02/testing-django-views-in-isolation/
# class SnippetCreateViewTest(TestCase):
#     """
#     Test the snippet create view
#     """
#     def setUp(self):
#         self.user = UserFactory()
#         self.factory = RequestFactory()
#     def test_get(self):
#         """
#         Test GET requests
#         """
#         request = self.factory.get(reverse('snippet_create'))
#         request.user = self.user
#         response = SnippetCreateView.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context_data['user'], self.user)
#         self.assertEqual(response.context_data['request'], request)

import pytest
import unittest
from django.urls import reverse

from django.test import Client

@pytest.mark.django_db
class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get(reverse('costcentrefilter'))
        if response.status_code == 302:
            self.assertIn ('login', response.url)
        else:
            self.assertEqual(response.status_code, 200)


