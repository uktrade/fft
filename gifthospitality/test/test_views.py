
from bs4 import BeautifulSoup

from django.test import (
    TestCase,
)
from django.urls import reverse

from core.test.test_base import RequestFactoryBase


class ViewGiftandHospitalityRegisterTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.client.login(
            username=self.test_user_email,
            password=self.test_password,
        )

    def test_user_can_see_g_h_tab(self):
        """
        Test user can view the Gifts and Hospitality tab on the homepage
        when assigned with 'superuser' permissions
        """

        self.test_user.is_superuser = True

        self.test_user.save()

        view_gifts_hospitality_tab = reverse(
            "index",
        )

        response = self.client.get(view_gifts_hospitality_tab)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        # print(soup)

        gifts_hospitality_links = soup.find_all("a", class_="hospitality")

        assert len(gifts_hospitality_links) == 1

    def test_user_cannot_see_g_h_tab(self):
        """
        Test basic user cannot view the Gifts and Hospitality tab on the homepage
        """

        view_gifts_hospitality_tab = reverse(
            "index",
        )

        response = self.client.get(view_gifts_hospitality_tab)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        # print(soup)

        gifts_hospitality_links = soup.find_all("a", class_="hospitality")

        assert len(gifts_hospitality_links) == 0
