from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from forecast.models import (
    FinancialPeriod,
)


class SetActualPeriodCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def clear_all_actual(self):
        FinancialPeriod.objects.all().update(actual_loaded=False)
        self.assertEqual(FinancialPeriod.objects.filter(actual_loaded=True).count(), 0)

    def clear_actual_period(self, period):
        # set the actual_loaded flag on all periods
        FinancialPeriod.objects.all().update(actual_loaded=True)
        self.assertEqual(FinancialPeriod.objects.filter(actual_loaded=False).count(), 0)
        call_command("set_actual_period", "--clear", period, stdout=self.out)
        self.assertEqual(
            FinancialPeriod.objects.filter(actual_loaded=True).count(), period - 1
        )

    def set_actual_period(self, period):
        # clear the actual_loaded flag on all periods
        FinancialPeriod.objects.all().update(actual_loaded=False)
        self.assertEqual(FinancialPeriod.objects.filter(actual_loaded=True).count(), 0)
        call_command("set_actual_period", period, stdout=self.out)
        self.assertEqual(
            FinancialPeriod.objects.filter(actual_loaded=True).count(), period
        )

    def test_clear_all_actuals(self):
        self.clear_actual_period(1)

    def test_clear_period_2_actuals(self):
        self.clear_actual_period(2)

    def test_clear_period_3_actuals(self):
        self.clear_actual_period(3)

    def test_clear_period_4_actuals(self):
        self.clear_actual_period(4)

    def test_clear_period_5_actuals(self):
        self.clear_actual_period(5)

    def test_clear_period_6_actuals(self):
        self.clear_actual_period(6)

    def test_clear_period_7_actuals(self):
        self.clear_actual_period(7)

    def test_clear_period_8_actuals(self):
        self.clear_actual_period(8)

    def test_clear_period_9_actuals(self):
        self.clear_actual_period(9)

    def test_clear_period_10_actuals(self):
        self.clear_actual_period(10)

    def test_clear_period_11_actuals(self):
        self.clear_actual_period(11)

    def test_clear_period_12_actuals(self):
        self.clear_actual_period(12)

    def test_clear_period_13_actuals(self):
        self.clear_actual_period(13)

    def test_clear_period_14_actuals(self):
        self.clear_actual_period(14)

    def test_clear_period_15_actuals(self):
        self.clear_actual_period(15)

    def test_set_period_1_actuals(self):
        self.set_actual_period(1)

    def test_set_period_2_actuals(self):
        self.set_actual_period(2)

    def test_set_period_3_actuals(self):
        self.set_actual_period(3)

    def test_set_period_4_actuals(self):
        self.set_actual_period(4)

    def test_set_period_5_actuals(self):
        self.set_actual_period(5)

    def test_set_period_6_actuals(self):
        self.set_actual_period(6)

    def test_set_period_7_actuals(self):
        self.set_actual_period(7)

    def test_set_period_8_actuals(self):
        self.set_actual_period(8)

    def test_set_period_9_actuals(self):
        self.set_actual_period(9)

    def test_set_period_10_actuals(self):
        self.set_actual_period(10)

    def test_set_period_11_actuals(self):
        self.set_actual_period(11)

    def test_set_period_12_actuals(self):
        self.set_actual_period(12)

    def test_set_period_13_actuals(self):
        self.set_actual_period(13)

    def test_set_period_14_actuals(self):
        self.set_actual_period(14)

    def test_set_period_15_actuals(self):
        self.set_actual_period(15)
