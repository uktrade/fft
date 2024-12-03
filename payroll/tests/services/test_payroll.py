import pytest

from core.models import FinancialYear
from payroll.services.payroll import employee_created, payroll_forecast_report

from ..factories import EmployeeFactory, PayElementTypeFactory


def test_payroll_forecast(db):
    # NOTE: These must match the PAYROLL.BASIC_PAY_NAC and PAYROLL.PENSION_NAC settings.
    SALARY_NAC = "71111001"
    PENSION_NAC = "71111002"

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

    # TODO: Consider an ergonomic way of avoiding this pattern all the time.
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

    financial_year = FinancialYear.objects.current()

    # In April, both employees are paid.
    # In May, only the first employee is paid.
    # In June, neither employee is paid.
    payroll_employees[0].pay_periods.filter(year=financial_year).update(period_3=False)
    payroll_employees[1].pay_periods.filter(year=financial_year).update(
        period_2=False, period_3=False
    )

    report = payroll_forecast_report(payroll_employees[0].cost_centre, financial_year)

    report_by_nac = {x["natural_account_code"]: x for x in report}

    # eN = employee (e.g. employee 1) / s = salary / p = pension
    # debit_amount - credit_amount
    e1s = (2000 - 100) + (100 - 50)
    e1p = 75.5 - 0
    e2s = (1500 - 55.6) + (80 - 0)
    e2p = 130.25 - 15

    # employee 3 and 4 are non-payroll (no basic pay)

    assert float(report_by_nac[SALARY_NAC]["apr"]) == pytest.approx(e1s + e2s)
    assert float(report_by_nac[PENSION_NAC]["apr"]) == pytest.approx(e1p + e2p)
    assert float(report_by_nac[SALARY_NAC]["may"]) == pytest.approx(e1s)
    assert float(report_by_nac[PENSION_NAC]["may"]) == pytest.approx(e1p)
    assert float(report_by_nac[SALARY_NAC]["jun"]) == pytest.approx(0)
    assert float(report_by_nac[PENSION_NAC]["jun"]) == pytest.approx(0)
