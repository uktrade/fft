import unittest

from bs4 import BeautifulSoup
from django.contrib.auth.models import Group
from django.urls import reverse

from core.test.test_base import BaseTestCase


@unittest.skip("Project Percentages has been removed from the nav bar")
class ViewSplitProjectTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

    def test_admin_user_can_view_project_split_page(self):
        self.test_user.is_superuser = True
        self.test_user.save()

        view_homepage = reverse(
            "index",
        )

        response = self.client.get(view_homepage)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        admin_link = soup.find_all("a", id="split_project")
        assert len(admin_link) == 1

    def test_project_admin_user_can_view_project_split_page(self):
        g = Group.objects.get(name="Project Split Administrator")
        g.user_set.add(self.test_user)
        view_homepage = reverse(
            "index",
        )
        response = self.client.get(view_homepage)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        admin_link = soup.find_all("a", id="split_project")
        assert len(admin_link) == 1

    def test_user_cannot_view_project_split_page(self):
        view_homepage = reverse(
            "index",
        )
        response = self.client.get(view_homepage)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        admin_link = soup.find_all("a", id="split_project")

        assert len(admin_link) == 0
