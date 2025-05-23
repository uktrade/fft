from bs4 import BeautifulSoup
from django.urls import reverse

from core.test.test_base import BaseTestCase
from gifthospitality.test.factories import GiftsAndHospitalityFactory


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

    def test_export_prevents_csv_injection(self):
        # given the user is a superuser
        self.test_user.is_superuser = True
        self.test_user.save()
        # and a gift and hospitality record exists with a csv injection
        GiftsAndHospitalityFactory(reason="=9+9")
        # when the user exports gift and hospitality records as a csv file
        url = reverse("gifthospitality:gift-search") + "?_export=csv"
        response = self.client.get(url)
        # then the csv injection is prevented
        assert "'=9+9" in response.content.decode("utf-8")
