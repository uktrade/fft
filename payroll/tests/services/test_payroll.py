from statistics import mean

import pytest

from core.models import FinancialYear
from costcentre.test.factories import CostCentreFactory
from payroll.services.payroll import (
    employee_created,
    payroll_forecast_report,
    vacancy_created,
)

from ..factories import EmployeeFactory, VacancyFactory


def test_payroll_forecast(db):
    # NOTE: These must match the PAYROLL.BASIC_PAY_NAC and PAYROLL.PENSION_NAC settings.
    SALARY_NAC = "71111001"
    PENSION_NAC = "71111002"

    cost_centre = CostCentreFactory.create(cost_centre_code="123456")

    payroll_employee_1 = EmployeeFactory.create(
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
        basic_pay=195000,
        pension=7550,
        ernic=0,
    )
    payroll_employee_2 = EmployeeFactory.create(
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
        basic_pay=152440,
        pension=11525,
        ernic=0,
    )
    # non-payroll employees
    _ = EmployeeFactory.create_batch(
        size=2,
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
    )

    # TODO: Consider an ergonomic way of avoiding this pattern all the time.
    employee_created(payroll_employee_1)
    employee_created(payroll_employee_2)

    vacancy = VacancyFactory.create(
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
        fte=0.5,
    )

    vacancy_created(vacancy)

    financial_year = FinancialYear.objects.current()

    # In April, both employees are paid.
    # In May, only the first employee is paid.
    # In June, neither employee is paid, but the vacancy is filled.
    payroll_employee_1.pay_periods.filter(year=financial_year).update(period_3=False)
    payroll_employee_2.pay_periods.filter(year=financial_year).update(
        period_2=False, period_3=False
    )
    vacancy.pay_periods.filter(year=financial_year).update(period_3=True)

    report = payroll_forecast_report(cost_centre, financial_year)

    report_by_nac = {x["natural_account_code"]: x for x in report}

    # eN = employee (e.g. employee 1) / s = salary / p = pension
    # debit_amount - credit_amount
    e1s = ((2000 - 100) + (100 - 50)) * 100
    e1p = (75.5 - 0) * 100
    e2s = ((1500 - 55.6) + (80 - 0)) * 100
    e2p = (130.25 - 15) * 100
    v1s = mean([e1s, e2s]) * 0.5

    # employee 3 and 4 are non-payroll (no basic pay)

    assert float(report_by_nac[SALARY_NAC]["apr"]) == pytest.approx(e1s + e2s)
    assert float(report_by_nac[PENSION_NAC]["apr"]) == pytest.approx(e1p + e2p)
    assert float(report_by_nac[SALARY_NAC]["may"]) == pytest.approx(e1s)
    assert float(report_by_nac[PENSION_NAC]["may"]) == pytest.approx(e1p)
    assert float(report_by_nac[SALARY_NAC]["jun"]) == pytest.approx(v1s)
    assert float(report_by_nac[PENSION_NAC]["jun"]) == pytest.approx(0)
