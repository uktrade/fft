import pytest

from django.contrib.auth.models import Group
from django.core.management import call_command

from costcentre.test.factories import CostCentreFactory, FinancialYearFactory
from user.models import User


@pytest.mark.parametrize(
    ["group_names", "status_code"],
    [
        # Not allowed to edit payroll
        ([], 403),
        (["Finance Administrator"], 403),
        # Allowed to edit payroll
        (["Finance Administrator", "Payroll Editor"], 200),
        (["Finance Administrator", "Payroll Admin"], 200),
    ],
)
def test_access_to_edit_payroll(client, user, group_names, status_code):
    call_command("manage_groups")

    FinancialYearFactory.create(financial_year=2024)
    CostCentreFactory.create(cost_centre_code="888812")

    url = "/payroll/edit/888812/2024/"

    groups = Group.objects.filter(name__in=group_names)
    user.groups.set(groups)

    user = User.objects.get(pk=user.pk)
    client.force_login(user)

    r = client.get(url)
    assert r.status_code == status_code
