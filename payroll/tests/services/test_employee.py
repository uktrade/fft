from core.test.factories import FinancialYearFactory
from payroll.services.employee import _build_employee_pay_periods
from payroll.tests.factories import EmployeeFactory


def test_build_employee_pay_periods(db):
    # given an employee without pay periods
    employee = EmployeeFactory()
    # and a current and future financial year
    current_year = FinancialYearFactory(financial_year=2020, current=True)
    future_year = FinancialYearFactory(financial_year=2021, current=False)

    # when `build_employee_pay_periods` is called for the current year
    current_pay_periods = _build_employee_pay_periods(
        employee=employee, year=current_year, period=6
    )

    # then we have false periods up until they were imported and true after
    assert current_pay_periods.periods == ([False] * 5) + ([True] * 7)

    # when `build_employee_pay_periods` is called for the future year
    future_pay_periods = _build_employee_pay_periods(
        employee=employee, year=future_year, period=6
    )

    # then we have all true periods
    assert future_pay_periods.periods == [True] * 12
