import unittest

from django.test import (
    Client,
)
from django.urls import reverse

import pytest

from core.utils.generic_helpers import get_current_financial_year
from core.test.test_base import BaseTestCase

from costcentre.test.factories import (
    ArchivedCostCentreFactory,
    BSCEFactory,
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
    FinanceBusinessPartnerFactory,
    FinancialYearFactory,
)


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


class ViewCostCentreTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076
        self.financial_year = FinancialYearFactory(financial_year=2019)
        self.name = "Test"
        self.surname = "FBP"
        self.bsce_email = "bsceuser@test.com"

        self.group = DepartmentalGroupFactory(
            group_code=self.group_code, group_name=self.group_name,
        )
        self.directorate = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=self.group,
        )

        self.business_partner = FinanceBusinessPartnerFactory(
            name=self.name,
            surname=self.surname,
        )

        self.bsce = BSCEFactory(
            bsce_email=self.bsce_email
        )

        self.cost_centre = CostCentreFactory(
            directorate=self.directorate,
            cost_centre_code=self.cost_centre_code,
            business_partner=self.business_partner,
            bsce_email=self.bsce,
        )

        self.archive_cost_centre = ArchivedCostCentreFactory(
            financial_year=self.financial_year,
            cost_centre_code=self.cost_centre_code,
        )

        current_year = get_current_financial_year()
        self.archive_year = current_year - 1

    def test_costcentre_view(self):
        url = (reverse("cost_centre_filter"))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check cost centre is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def test_costcentre_download(self):
        url = reverse("cost_centre_filter",)
        # add the argument required for downloading to excel
        url = f"{url}?_export=xlsx"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_archive_costcentre_view(self):
        response = self.client.get(
            reverse(
                "historical_cost_centre_filter",
                kwargs={"year": self.archive_year},
            ),
        )

        self.assertEqual(response.status_code, 200)

        # Check cost centre is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def test_archive_costcentre_download(self):
        url = reverse("historical_cost_centre_filter",
                      kwargs={"year": self.archive_year},)
        url = f"{url}?_export=xlsx"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_fbp_bsce_view(self):
        url = reverse("cost_centre_filter",)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        assert str(self.business_partner) in str(response.rendered_content)
        assert str(self.bsce) in str(response.rendered_content)

    def test_group_directorate_view(self):
        url = reverse("cost_centre_filter",)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        assert str(self.group) in str(response.rendered_content)
        assert str(self.directorate) in str(response.rendered_content)
