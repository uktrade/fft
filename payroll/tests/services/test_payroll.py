import pytest

from ..factories import (
    EmployeeFactory,
    PayElementTypeGroupFactory,
    PayElementTypeFactory,
    PayElementType,
    PayElementTypeGroup,
)


def test_payroll_forecast(db):
    SALARY_NAC = "77770001"
    PENSION_NAC = "77770002"

    PayElementTypeFactory.create(
        name="Salary 1",
        group__name="Salary",
        group__natural_code__natural_account_code=SALARY_NAC,
    )
    PayElementTypeFactory.create(
        name="Salary 2",
        group__name="Salary",
        group__natural_code__natural_account_code=SALARY_NAC,
    )
    PayElementTypeFactory.create(
        name="Pension 1",
        group__name="Pension",
        group__natural_code__natural_account_code=PENSION_NAC,
    )

    payroll_employees = EmployeeFactory.create_batch(
        size=2,
        cost_centre__cost_centre_code="123456",
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
    )
    non_payroll_employees = EmployeeFactory.create_batch(
        size=2,
        cost_centre__cost_centre_code="123456",
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
    )

    expected = (
        # employee 1
        (2000 - 100)  # salary_1 debit - credit
        + (100 - 50)  # + salary_2 debit - credit
        + (75.5 - 0)  # + pension debit - credit
        # employee 2
        + (1500 - 55.6)  # salary_1 debit - credit
        + (80 - 0)  # + salary_2 debit - credit
        + (130.25 - 15)  # + pension debit - credit
        # employee 3 and 4 are non-payroll (no basic pay)
    )
    assert expected == 3665.15
