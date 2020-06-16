from bs4 import BeautifulSoup

from django.test import (
    TestCase,
)
from django.urls import reverse

from core.test.test_base import RequestFactoryBase

from gifthospitality.forms import GiftAndHospitalityOfferedForm,\
    GiftAndHospitalityReceivedForm
from gifthospitality.models import DepartmentalGroup, GiftAndHospitality,\
    GiftAndHospitalityCategory, GiftAndHospitalityClassification,\
    GiftAndHospitalityCompany, Grade


class GiftHospitalityFormTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.client.login(
            username=self.test_user_email,
            password=self.test_password,
        )

        self.classification = GiftAndHospitalityClassification(sequence_no="10",
                                                               gif_hospitality_classification="98", # noqa
                                                               active=True)
        self.classification.save()

        self.category = GiftAndHospitalityCategory(sequence_no="10",
                                                   gif_hospitality_category="10",
                                                   active=True)
        self.category.save()

        grade = Grade(grade="Test", gradedescription="Test Grade")
        grade.save()

        departmental_group = DepartmentalGroup(group_code="8888AA", group_name="8888AA")
        departmental_group.save()

        self.company = GiftAndHospitalityCompany(sequence_no="10",
                                                 gif_hospitality_company="10",
                                                 active=True)
        self.company.save()

        action_taken = GiftAndHospitality(action_taken="Action1",
                                          date_agreed="2006-05-23",
                                          value="12",
                                          entered_date_stamp="2020-05-22",
                                          # category_id="1",
                                          # classification_id="3",
                                          classification=self.classification,
                                          category=self.category,)
        action_taken.save()

    def test_gift_hospitality_receive_form(self):
        response = reverse("gifthospitality:gift-received",)

        response = self.client.get(response)

        self.assertEqual(response.status_code, 200)

        grade_filter = Grade.objects.get(grade="Test").grade

        group_filter = DepartmentalGroup.objects.get(group_code="8888AA").group_code

        action_taken_filter = GiftAndHospitality.objects.get(
            action_taken="Action1").date_agreed

        gift_hospitality_received_data = {
            'classification': self.classification.pk,
            'category': self.category.pk,
            'date_agreed_0': action_taken_filter.day,
            'date_agreed_1': action_taken_filter.month,
            'date_agreed_2': action_taken_filter.year,
            'action_taken': 'Action1',
            'venue': 'Normal Venue',
            'reason': 'Recommended by FD',
            'value': '12',
            'rep': 'Someone from DIT',
            'grade': grade_filter,
            'group': group_filter,
            'company_rep': 'Someone from a company',
            'company': self.company.pk,
            'company_name': '',
        }

        self.assertContains(response, "govuk-button")

        gift_hospitality_received_form = GiftAndHospitalityReceivedForm(
            data=gift_hospitality_received_data)

        assert gift_hospitality_received_form.is_valid()

    def test_gift_hospitality_offered_form(self):
        response = reverse("gifthospitality:gift-offered",)

        response = self.client.get(response)

        self.assertEqual(response.status_code, 200)

        grade_filter = Grade.objects.get(grade="Test").grade

        group_filter = DepartmentalGroup.objects.get(group_code="8888AA").group_code

        action_taken_filter = GiftAndHospitality.objects.get(
            action_taken="Action1").date_agreed

        gift_hospitality_offered_data = {
            'classification': self.classification.pk,
            'category': self.category.pk,
            'date_agreed_0': action_taken_filter.day,
            'date_agreed_1': action_taken_filter.month,
            'date_agreed_2': action_taken_filter.year,
            'action_taken': 'Action1',
            'venue': 'Normal Venue',
            'reason': 'Recommended by FD',
            'value': '12',
            'rep': 'Someone from DIT',
            'grade': grade_filter,
            'group': group_filter,
            'company_rep': 'Someone from a company',
            'company': self.company.pk,
            'company_name': '',
        }

        self.assertContains(response, "govuk-button")

        gift_hospitality_offered_form = GiftAndHospitalityOfferedForm(
            data=gift_hospitality_offered_data)

        assert gift_hospitality_offered_form.is_valid()

    def test_search_records(self):

        self.test_user.is_superuser = True
        self.test_user.save()

        response = reverse("gifthospitality:gift-search", )

        response = self.client.get(response)

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, features="html.parser")

        record_id = soup.find_all('td')

        self.assertTrue(record_id)

        download_search_records_url = self.client.get("gifthospitality:?_export.xlsx")
        self.assertEqual(download_search_records_url.status_code, 200)
