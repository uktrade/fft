import json

import waffle.testutils
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.urls import reverse

from config import flags
from costcentre.test.factories import CostCentreFactory
from payroll.models import EmployeePayPeriods
from payroll.tests.factories import (
    EmployeeFactory,
    EmployeePayPeriodsFactory,
    FinancialYearFactory,
)


@waffle.testutils.override_flag(flags.EDIT_PAYROLL, active=True)
def test_update_notes_faulty_json(db, client, user):
    call_command("manage_groups")

    admin_group = Group.objects.get(name="Finance Administrator")
    user.groups.add(admin_group)
    client.force_login(user)

    FinancialYearFactory.create(financial_year=2024)
    CostCentreFactory.create(cost_centre_code="888813")
    url = reverse(
        "payroll:employee_notes",
        kwargs={"cost_centre_code": "888813", "financial_year": 2024},
    )

    response = client.post(
        url,
        data="some string",
        content_type="application/json",
    )
    assert url == "/payroll/api/888813/2024/employees/notes"
    assert response.status_code == 400


@waffle.testutils.override_flag(flags.EDIT_PAYROLL, active=True)
def test_update_notes_fail(db, client, user):
    call_command("manage_groups")

    admin_group = Group.objects.get(name="Finance Administrator")
    user.groups.add(admin_group)
    client.force_login(user)

    FinancialYearFactory.create(financial_year=2024)
    CostCentreFactory.create(cost_centre_code="888813")
    url = reverse(
        "payroll:employee_notes",
        kwargs={"cost_centre_code": "888813", "financial_year": 2024},
    )

    response = client.post(
        url,
        data=json.dumps({"notes": "some notes"}),
        content_type="application/json",
    )
    assert response.status_code == 400


@waffle.testutils.override_flag(flags.EDIT_PAYROLL, active=True)
def test_update_notes_success(db, client, user):
    call_command("manage_groups")
    data = {
        "notes": "some notes",
        "id": "150892",
    }
    admin_group = Group.objects.get(name="Finance Administrator")
    user.groups.add(admin_group)
    client.force_login(user)
    cost_centre = CostCentreFactory.create(cost_centre_code="888813")
    employee = EmployeeFactory.create(
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
        basic_pay=195000,
        pension=7550,
        ernic=0,
        id=data.get("id"),
    )
    EmployeePayPeriodsFactory(year_id=2024, employee=employee)
    FinancialYearFactory.create(financial_year=2024)

    url = reverse(
        "payroll:employee_notes",
        kwargs={"cost_centre_code": "888813", "financial_year": 2024},
    )

    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )
    pay_period = EmployeePayPeriods.objects.filter(
        employee=employee,
        year=2024,
    ).first()

    assert response.status_code == 200
    assert pay_period.notes == data.get("notes")
