from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from gifthospitality.models import (
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
    Grade,
)


class GiftsHospitalityCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_g_and_h_not_imported(self):
        self.assertFalse(GiftAndHospitalityCompany.objects.filter(
            sequence_no=10).exists())
        self.assertFalse(GiftAndHospitalityCategory.objects.filter(
            sequence_no=10).exists())
        self.assertFalse(GiftAndHospitalityClassification.objects.filter(
            sequence_no=10).exists())
        self.assertFalse(Grade.objects.filter(grade='SEO').exists())

    def test_g_and_h_imported(self):
        call_command(
            "populate_gift_hospitality_table",
        )
        self.assertTrue(GiftAndHospitalityCompany.objects.filter(
            sequence_no=10).exists())
        self.assertTrue(GiftAndHospitalityCategory.objects.filter(
            sequence_no=10).exists())
        self.assertTrue(GiftAndHospitalityClassification.objects.filter(
            sequence_no=10).exists())
        self.assertTrue(Grade.objects.filter(grade='SEO').exists())
