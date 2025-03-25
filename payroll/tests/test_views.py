import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command

from costcentre.test.factories import CostCentreFactory, FinancialYearFactory
from forecast.permission_shortcuts import assign_perm
from user.models import User


@pytest.mark.parametrize(
    ["group_names", "cost_centres", "status_code"],
    [
        # Not allowed to edit payroll
        ([], [], 403),
        (["Finance Business Partner/BSCE"], [], 403),
        # Allowed to edit payroll
        (["Finance Administrator"], [], 200),
        (["Finance Business Partner/BSCE"], ["888812"], 200),
    ],
)
def test_access_to_edit_payroll(client, user, group_names, cost_centres, status_code):
    call_command("manage_groups")

    FinancialYearFactory.create(financial_year=2024)
    CostCentreFactory.create(cost_centre_code="888812")

    url = "/payroll/edit/888812/2024/"

    groups = Group.objects.filter(name__in=group_names)
    user.groups.set(groups)

    for cost_centre_code in cost_centres:
        cost_centre_obj = CostCentreFactory(cost_centre_code=cost_centre_code)
        assign_perm("change_costcentre", user, cost_centre_obj)

    user = User.objects.get(pk=user.pk)
    client.force_login(user)

    r = client.get(url)
    assert r.status_code == status_code
