from core.models import FinancialYear
from core.types import MonthIndex
from payroll.models import Employee, EmployeePayPeriods


def employee_joined(employee: Employee, year: FinancialYear, month: MonthIndex) -> None:
    """Hook to be called after an employee has joined payroll."""
    # Create EmployeePayPeriods records for current and future financial years.
    for year in FinancialYear.objects.forecast():
        _build_employee_pay_periods(employee=employee, year=year, period=month).save()


def employee_rejoined(
    employee: Employee, year: FinancialYear, month: MonthIndex
) -> None:
    """Hook to be called after an employee has rejoined payroll."""
    employee.has_left = False
    employee.save()

    pay_periods = employee.pay_periods.filter(year=year).first()
    pay_periods.set_periods_from_month(month, True)
    pay_periods.save()


def employee_has_left(
    employee: Employee, year: FinancialYear, month: MonthIndex
) -> None:
    """Hook to be called after an employee has left payroll.

    Args:
        employee: The employee which has left.
        year: Which year the employee left.
        month: Which month the employee left.
    """
    employee.has_left = True
    employee.save()

    pay_periods = employee.pay_periods.filter(year=year).first()
    pay_periods.set_periods_from_month(month, False)
    pay_periods.save()


def _build_employee_pay_periods(
    *, employee: Employee, year: FinancialYear, period: int
) -> EmployeePayPeriods:
    periods = [employee.is_payroll] * 12

    if year.current:
        periods = ([False] * (period - 1)) + periods[period - 1 :]

    obj = EmployeePayPeriods(employee=employee, year=year)
    obj.periods = periods

    return obj
