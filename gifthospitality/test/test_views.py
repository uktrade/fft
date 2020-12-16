
from bs4 import BeautifulSoup

from django.urls import reverse

from core.test.test_base import BaseTestCase


class ViewGiftandHospitalityRegisterTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

    def test_user_can_see_g_h_tab(self):
        """
        Test basic user can view the Gifts and Hospitality tab on the homepage
        """

        view_gifts_hospitality_tab = reverse(
            "index",
        )

        response = self.client.get(view_gifts_hospitality_tab)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")
        gifts_hospitality_links = soup.find_all("a", class_="hospitality")

        assert len(gifts_hospitality_links) == 1
