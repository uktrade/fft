from django.contrib.auth import get_user_model
from django.test import TestCase

from payroll.templatetags.payroll_permissions import can_access_edit_payroll


class ViewPayrollTest(TestCase):
    def test_can_access_edit_payroll_when_superuser(self):
        test_user, _ = get_user_model().objects.get_or_create(is_superuser=True)

        assert can_access_edit_payroll(test_user)

    def test_cannot_access_edit_payroll_when_not_superuser(self):
        test_user, _ = get_user_model().objects.get_or_create()

        assert not can_access_edit_payroll(test_user)
