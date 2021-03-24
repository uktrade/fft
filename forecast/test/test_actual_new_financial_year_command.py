from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from forecast.models import FinancialPeriod


class ActualNewFinancialYearCommandTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_actual_new_financial_year(self):
        FinancialPeriod.objects.all().update(actual_loaded=True)
        actual_count = FinancialPeriod.objects.filter(actual_loaded=True).count()
        assert (
            FinancialPeriod.objects.filter(actual_loaded_previous_year=True).count()
            == 0
        )
        call_command("actual_new_financial_year", stdout=self.out)
        assert FinancialPeriod.objects.filter(actual_loaded=True).count() == 0
        assert (
            actual_count
            == FinancialPeriod.objects.filter(actual_loaded_previous_year=True).count()
        )
