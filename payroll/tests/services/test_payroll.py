from decimal import Decimal
import pytest

from core.models import FinancialYear
from payroll.models import EmployeePayElement
from payroll.services.payroll import employee_created, payroll_forecast_report

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

    salary_1 = PayElementTypeFactory.create(
        name="Salary 1",
        group__name="Salary",
        group__natural_code__natural_account_code=SALARY_NAC,
    )
    salary_2 = PayElementTypeFactory.create(
        name="Salary 2",
        group__name="Salary",
        group__natural_code__natural_account_code=SALARY_NAC,
    )
    pension_1 = PayElementTypeFactory.create(
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
    # non-payroll employees
    _ = EmployeeFactory.create_batch(
        size=2,
        cost_centre__cost_centre_code="123456",
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
    )

    for x in payroll_employees:
        employee_created(x)

    payroll_employees[0].pay_element.create(
        type=salary_1,
        debit_amount=2000,
        credit_amount=100,
    )
    payroll_employees[0].pay_element.create(
        type=salary_2,
        debit_amount=100,
        credit_amount=50,
    )
    payroll_employees[0].pay_element.create(
        type=pension_1,
        debit_amount=75.5,
        credit_amount=0,
    )

    payroll_employees[1].pay_element.create(
        type=salary_1,
        debit_amount=1500,
        credit_amount=55.6,
    )
    payroll_employees[1].pay_element.create(
        type=salary_2,
        debit_amount=80,
        credit_amount=0,
    )
    payroll_employees[1].pay_element.create(
        type=pension_1,
        debit_amount=130.25,
        credit_amount=15,
    )

    report = payroll_forecast_report(
        payroll_employees[0].cost_centre, FinancialYear.objects.current()
    )

    report_by_name = {x["pay_element__type__group__name"]: x for x in report}

    expected_salary = (
        # employee 1
        (2000 - 100)  # salary_1 debit - credit
        + (100 - 50)  # + salary_2 debit - credit
        # employee 2
        + (1500 - 55.6)  # salary_1 debit - credit
        + (80 - 0)  # + salary_2 debit - credit
    )
    expected_pension = (
        # employee 1
        (75.5 - 0)  # + pension debit - credit
        # employee 2
        + (130.25 - 15)  # + pension debit - credit
    )

    # employee 3 and 4 are non-payroll (no basic pay)

    assert float(report_by_name["Salary"]["period_1_sum"]) == pytest.approx(
        expected_salary
    )
    assert float(report_by_name["Pension"]["period_1_sum"]) == pytest.approx(
        expected_pension
    )
