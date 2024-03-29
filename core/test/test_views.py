from bs4 import BeautifulSoup
from django.urls import reverse

from core.test.test_base import BaseTestCase


class ViewAdminLink(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

    def test_user_can_view_admin_link(self):
        """
        Test admin user can view Admin link in navigation bar
        """
        # Create staff user
        self.test_user.is_staff = True
        self.test_user.save()

        view_homepage = reverse(
            "index",
        )

        response = self.client.get(view_homepage)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        admin_link = soup.find_all("a", id="admin_page")

        assert len(admin_link) == 1

    def test_user_cannot_view_admin_link(self):
        """
        Test admin user cannot view Admin link in navigation bar
        """

        view_homepage = reverse(
            "index",
        )

        response = self.client.get(view_homepage)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        admin_link = soup.find_all("a", id="admin_page")

        assert len(admin_link) == 0
