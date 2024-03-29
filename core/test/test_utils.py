from django.contrib.admin.models import LogEntry

from core.models import FinancialYear
from core.test.test_base import BaseTestCase
from core.utils.generic_helpers import log_object_change


class ViewUtils(BaseTestCase):
    def test_log_object_change_no_object(self):
        log_object_change(
            self.test_user.id,
            "test",
        )

        log_entry = LogEntry.objects.last()

        assert log_entry.change_message == "test"

    def test_log_object_change_with_object(self):
        financial_year = FinancialYear.objects.last()

        log_object_change(
            self.test_user.id,
            "test",
            obj=financial_year,
        )

        log_entry = LogEntry.objects.last()

        assert log_entry.change_message == f"{str(financial_year)} test"
        assert log_entry.object_id == str(financial_year.pk)
