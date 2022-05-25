from io import StringIO

from django.test import TestCase
from django.core.management import call_command

from end_of_month.test.test_utils import MonthlyFigureSetup

from forecast.models import (
    FinancialCode,
)
from forecast.test.factories import FinancialCodeFactory

class ClearForecastCommandNoArchiveTest(TestCase):
    def setUp(self):
        self.out = StringIO()
        init_data = MonthlyFigureSetup()
        init_data.setup_forecast()
        init_data.setup_budget()
        FinancialCodeFactory()

    def test_dont_remove_in_use(self):
        assert FinancialCode.objects.all().count() == 2
        call_command("clear_financial_codes")
        assert FinancialCode.objects.all().count() == 1
