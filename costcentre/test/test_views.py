import unittest

from django.test import (
    Client,
    TestCase
)
from django.urls import reverse

import pytest

from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)
from costcentre.views import FilteredCostListView


@pytest.mark.django_db
class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get(reverse("cost_centre_filter"))
        # if redirecting, check that we are sending to a login page
        if response.status_code == 302:
            self.assertIn("login", response.url)
        else:
            self.assertEqual(response.status_code, 200)


class ViewCostCentreTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

        self.group = DepartmentalGroupFactory(
            group_code=self.group_code, group_name=self.group_name,
        )
        self.directorate = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=self.group,
        )
        self.cost_centre = CostCentreFactory(
            directorate=self.directorate, cost_centre_code=self.cost_centre_code,
        )

    def test_costcentre_view(self):
        url = (reverse("cost_centre_filter",),)

        response = self.factory_get(url, FilteredCostListView,)
        self.assertEqual(response.status_code, 200)

        # Check cost centre is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def test_costcentre_download(self):
        url = reverse("cost_centre_filter",)
        # add the argument required for downloading to excel
        url = f"{url}?_export=xlsx"
        print(url)
        response = self.factory_get(url, FilteredCostListView,)
        self.assertEqual(response.status_code, 200)
