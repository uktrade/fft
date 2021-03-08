from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from core.models import FinancialYear


class SetCurrentYearCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_set_current_year(self):
        # set the actual_loaded flag on all periods
        self.assertEqual(FinancialYear.objects.filter(current=True).count(), 1)
        financial_year_before = FinancialYear.objects.get(current=True).financial_year
        call_command("set_current_year", financial_year_before + 1, stdout=self.out)
        financial_year_after = FinancialYear.objects.get(current=True).financial_year
        self.assertNotEqual(financial_year_after, financial_year_before)
        self.assertEqual(financial_year_after, financial_year_before + 1)

    def test_set_and_create_current_year(self):
        self.assertEqual(FinancialYear.objects.filter(current=True).count(), 1)
        financial_year_before = FinancialYear.objects.get(current=True).financial_year
        new_financial_year = 2028
        self.assertEqual(
            FinancialYear.objects.filter(financial_year=new_financial_year).count(), 0
        )
        call_command("set_current_year", new_financial_year, stdout=self.out)
        self.assertEqual(
            FinancialYear.objects.filter(financial_year=new_financial_year).count(), 1
        )
        financial_year_after = FinancialYear.objects.get(current=True).financial_year
        self.assertNotEqual(financial_year_after, financial_year_before)
        self.assertEqual(financial_year_after, new_financial_year)
