from math import floor
from random import randrange
from statistics import mean

import pytest

from chartofaccountDIT.test.factories import ProgrammeCodeFactory
from core.constants import MONTHS
from core.models import FinancialYear
from core.test.factories import FinancialYearFactory
from core.types import MonthsDict
from core.utils.generic_helpers import get_previous_months_data
from costcentre.test.factories import CostCentreFactory
from forecast.models import FinancialPeriod, ForecastMonthlyFigure
from forecast.test.factories import FinancialCodeFactory
from gifthospitality.test.factories import GradeFactory
from payroll.services.employee import employee_joined
from payroll.services.payroll import (
    EmployeeCost,
    PayrollForecast,
    get_average_cost_for_grade,
    payroll_forecast_report,
    update_payroll_forecast,
    update_payroll_forecast_figure,
)
from payroll.services.vacancy import vacancy_created

from ..factories import (
    AttritionFactory,
    EmployeeFactory,
    PayUpliftFactory,
    VacancyFactory,
)


# NOTE: These must match the PAYROLL.BASIC_PAY_NAC, PAYROLL.PENSION_NAC and PAYROLL.ERNIC_NAC settings.
SALARY_NAC = 71111001
PENSION_NAC = 71111002
ERNIC_NAC = 71111003
NACS = [SALARY_NAC, PENSION_NAC, ERNIC_NAC]


def assert_report_results_with_modifiers(
    report, salary, pension, ernic, modifiers=None
):
    if modifiers is None:
        modifiers = {}

    for nac in NACS:
        for month in MONTHS:
            modifier = modifiers.get(month, 1)
            if nac == SALARY_NAC:
                expected_result = salary * modifier
            elif nac == PENSION_NAC:
                expected_result = pension * modifier
            else:
                expected_result = ernic * modifier

            assert float(report[nac][month]) == pytest.approx(floor(expected_result))


def test_payroll_forecast(db, payroll_nacs):
    cost_centre = CostCentreFactory(cost_centre_code="123456")

    payroll_employee_1 = EmployeeFactory.create(
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
        basic_pay=1950_00,
        pension=75_50,
        ernic=62_75,
    )
    payroll_employee_2 = EmployeeFactory.create(
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
        basic_pay=1524_40,
        pension=115_25,
        ernic=42_30,
    )
    # non-payroll employees
    _ = EmployeeFactory.create_batch(
        size=2,
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
        basic_pay=0,
        pension=0,
        ernic=0,
    )

    financial_year = FinancialYear.objects.current()

    # TODO: Consider an ergonomic way of avoiding this pattern all the time.
    employee_joined(employee=payroll_employee_1, year=financial_year, month=1)
    employee_joined(employee=payroll_employee_2, year=financial_year, month=1)

    vacancy = VacancyFactory.create(
        cost_centre=cost_centre,
        programme_code__programme_code="123456",
        grade__grade="Grade 7",
        fte=0.5,
    )

    vacancy_created(vacancy)

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

    # eN = employee (e.g. employee 1) / s = salary / p = pension / e = ernic
    # debit_amount - credit_amount
    e1s = ((2000 - 100) + (100 - 50)) * 100
    e1e = 6275
    e1p = (75.5 - 0) * 100
    e2s = ((1500 - 55.6) + (80 - 0)) * 100
    e2p = (130.25 - 15) * 100
    e2e = 4230
    v1s = mean([e1s, e2s]) * 0.5
    v1p = mean([e1p, e2p]) * 0.5
    v1e = mean([e1e, e2e]) * 0.5

    # employee 3 and 4 are non-payroll (no basic pay)

    assert float(report_by_nac[SALARY_NAC]["apr"]) == pytest.approx(floor(e1s + e2s))
    assert float(report_by_nac[PENSION_NAC]["apr"]) == pytest.approx(floor(e1p + e2p))
    assert float(report_by_nac[ERNIC_NAC]["apr"]) == pytest.approx(floor(e1e + e2e))
    assert float(report_by_nac[SALARY_NAC]["may"]) == pytest.approx(floor(e1s))
    assert float(report_by_nac[PENSION_NAC]["may"]) == pytest.approx(floor(e1p))
    assert float(report_by_nac[ERNIC_NAC]["may"]) == pytest.approx(floor(e1e))
    assert float(report_by_nac[SALARY_NAC]["jun"]) == pytest.approx(floor(v1s))
    assert float(report_by_nac[PENSION_NAC]["jun"]) == pytest.approx(floor(v1p))
    assert float(report_by_nac[ERNIC_NAC]["jun"]) == pytest.approx(floor(v1e))


def test_one_employee_with_no_modifiers(db, current_financial_year, payroll_nacs):
    cost_centre = CostCentreFactory(cost_centre_code="123456")

    payroll_employee_1 = EmployeeFactory(
        cost_centre=cost_centre,
        basic_pay=195000,
        pension=7550,
        ernic=2000,
    )

    employee_joined(employee=payroll_employee_1, year=current_financial_year, month=1)

    report = payroll_forecast_report(cost_centre, current_financial_year)

    report_by_nac = {x["natural_account_code"]: x for x in report}

    e1s = ((2000 - 100) + (100 - 50)) * 100
    e1p = (75.5 - 0) * 100
    e1e = payroll_employee_1.ernic

    assert_report_results_with_modifiers(report_by_nac, e1s, e1p, e1e)


def test_one_employee_with_pay_uplift(db, current_financial_year, payroll_nacs):
    cost_centre = CostCentreFactory(cost_centre_code="123456")

    payroll_employee_1 = EmployeeFactory.create(
        cost_centre=cost_centre,
        basic_pay=195000,
        pension=7550,
        ernic=2000,
    )

    employee_joined(employee=payroll_employee_1, year=current_financial_year, month=1)

    pay_uplift = PayUpliftFactory.create(
        financial_year=current_financial_year,
        aug=0.02,
    )
    modifier = 1 + pay_uplift.aug

    report = payroll_forecast_report(cost_centre, current_financial_year)

    report_by_nac = {x["natural_account_code"]: x for x in report}

    e1s = ((2000 - 100) + (100 - 50)) * 100
    e1p = (75.5 - 0) * 100
    e1e = payroll_employee_1.ernic

    assert_report_results_with_modifiers(
        report_by_nac,
        e1s,
        e1p,
        e1e,
        modifiers={
            "aug": modifier,
            "sep": modifier,
            "oct": modifier,
            "nov": modifier,
            "dec": modifier,
            "jan": modifier,
            "feb": modifier,
            "mar": modifier,
        },
    )


def test_one_employee_with_attrition(db, current_financial_year, payroll_nacs):
    cost_centre = CostCentreFactory(cost_centre_code="123456")

    payroll_employee_1 = EmployeeFactory.create(
        cost_centre=cost_centre,
        basic_pay=195000,
        pension=7550,
        ernic=2000,
    )

    employee_joined(employee=payroll_employee_1, year=current_financial_year, month=1)

    attrition = AttritionFactory.create(
        cost_centre=cost_centre,
        financial_year=current_financial_year,
        aug=0.05,
    )
    modifier = 1 - attrition.aug

    report = payroll_forecast_report(cost_centre, current_financial_year)

    report_by_nac = {x["natural_account_code"]: x for x in report}

    e1s = ((2000 - 100) + (100 - 50)) * 100
    e1p = (75.5 - 0) * 100
    e1e = payroll_employee_1.ernic

    assert_report_results_with_modifiers(
        report_by_nac,
        e1s,
        e1p,
        e1e,
        modifiers={
            "aug": modifier,
            "sep": modifier,
            "oct": modifier,
            "nov": modifier,
            "dec": modifier,
            "jan": modifier,
            "feb": modifier,
            "mar": modifier,
        },
    )


def test_update_payroll_forecast_figure(db):
    cost_centre = CostCentreFactory(cost_centre_code="123456")
    programme_code = ProgrammeCodeFactory()

    financial_code_salary = FinancialCodeFactory(
        cost_centre=cost_centre,
        programme=programme_code,
        natural_account_code__natural_account_code=SALARY_NAC,
    )

    financial_year = FinancialYear.objects.current()

    expected_forecast: MonthsDict[int] = dict(
        # pence
        apr=randrange(0, 1_000_000),
        may=randrange(0, 1_000_000),
        jun=randrange(0, 1_000_000),
        jul=randrange(0, 1_000_000),
        aug=randrange(0, 1_000_000),
        sep=randrange(0, 1_000_000),
        oct=randrange(0, 1_000_000),
        nov=randrange(0, 1_000_000),
        dec=randrange(0, 1_000_000),
        jan=randrange(0, 1_000_000),
        feb=randrange(0, 1_000_000),
        mar=randrange(0, 1_000_000),
    )

    payroll_forecast = PayrollForecast(
        programme_code=programme_code,
        natural_account_code=SALARY_NAC,
        **expected_forecast,
    )

    update_payroll_forecast_figure(
        financial_year=financial_year,
        cost_centre=cost_centre,
        payroll_forecast=payroll_forecast,
    )

    forecast_figures = (
        ForecastMonthlyFigure.objects.filter(
            financial_year=financial_year,
            financial_code=financial_code_salary,
            archived_status=None,
        )
        .order_by("financial_period")
        .values_list("amount", flat=True)
    )

    assert list(forecast_figures) == list(expected_forecast.values())


def test_update_payroll_forecast_skips_overseas_cost_centre(
    db, current_financial_year, payroll_nacs
):
    # given an overseas cost centre
    cost_centre = CostCentreFactory(is_overseas=True)
    # and an employee on payroll
    employee = EmployeeFactory(
        cost_centre=cost_centre,
        basic_pay=2000,
        pension=160,
        ernic=120,
    )
    employee_joined(employee=employee, year=current_financial_year, month=1)

    financial_code_salary = FinancialCodeFactory(
        cost_centre=employee.cost_centre,
        programme=employee.programme_code,
        natural_account_code__natural_account_code=SALARY_NAC,
    )

    # when the payroll forecast is updated
    update_payroll_forecast(
        financial_year=current_financial_year,
        cost_centre=employee.cost_centre,
    )

    forecast_figures = (
        ForecastMonthlyFigure.objects.filter(
            financial_year=current_financial_year,
            financial_code=financial_code_salary,
            archived_status=None,
        )
        .order_by("financial_period")
        .values_list("amount", flat=True)
    )

    # then the forecast is not updated
    assert not forecast_figures


def test_average_cost_for_grade(db):
    # 2 cost centres in different directorates
    cost_centre_1 = CostCentreFactory(
        cost_centre_code="000001", directorate__directorate_code="000001"
    )
    cost_centre_2 = CostCentreFactory(
        cost_centre_code="000002", directorate__directorate_code="000002"
    )
    grade = GradeFactory()

    EmployeeFactory(
        cost_centre=cost_centre_1,
        grade=grade,
        basic_pay=200000,
        ernic=18000,
        pension=40000,
    )
    EmployeeFactory(
        cost_centre=cost_centre_1,
        grade=grade,
        basic_pay=250000,
        ernic=22000,
        pension=60000,
    )
    # This employee won't be factored into the calculations.
    EmployeeFactory(
        cost_centre=cost_centre_2,
        grade=grade,
        basic_pay=300000,
        ernic=27000,
        pension=70000,
    )

    employee_cost = get_average_cost_for_grade(grade=grade, cost_centre=cost_centre_1)
    expected = EmployeeCost(
        basic_pay=225000,
        ernic=20000,
        pension=50000,
    )
    assert employee_cost == expected


def test_update_all_payroll_forecast_removes_orphaned_figures(
    db, current_financial_year, payroll_nacs
):
    prog_1 = ProgrammeCodeFactory(programme_code="123456")
    prog_2 = ProgrammeCodeFactory(programme_code="654321")

    employee = EmployeeFactory(programme_code=prog_1)
    employee_joined(employee=employee, year=current_financial_year, month=1)

    payroll_fin_code_1 = FinancialCodeFactory(
        cost_centre=employee.cost_centre,
        programme=prog_1,
        natural_account_code__natural_account_code=SALARY_NAC,
    )
    payroll_fin_code_2 = FinancialCodeFactory(
        cost_centre=employee.cost_centre,
        programme=prog_2,
        natural_account_code__natural_account_code=SALARY_NAC,
    )

    # create a forecast against a non-payroll NAC
    other_fin_code = FinancialCodeFactory(
        cost_centre=employee.cost_centre,
        programme=prog_2,
    )
    ForecastMonthlyFigure.objects.create(
        financial_year=current_financial_year,
        financial_period_id=1,
        financial_code=other_fin_code,
        amount=999_99,
    )

    update_payroll_forecast(
        financial_year=current_financial_year,
        cost_centre=employee.cost_centre,
    )

    # move all employee's to a different programme code
    employee.programme_code = prog_2
    employee.save()

    update_payroll_forecast(
        financial_year=current_financial_year,
        cost_centre=employee.cost_centre,
    )

    forecast_figures_1 = (
        ForecastMonthlyFigure.objects.filter(
            financial_year=current_financial_year,
            financial_code=payroll_fin_code_1,
            archived_status=None,
        )
        .order_by("financial_period")
        .values_list("amount", flat=True)
    )
    forecast_figures_2 = (
        ForecastMonthlyFigure.objects.filter(
            financial_year=current_financial_year,
            financial_code=payroll_fin_code_2,
            archived_status=None,
        )
        .order_by("financial_period")
        .values_list("amount", flat=True)
    )

    # orphan forecasts have been removed
    assert list(forecast_figures_1) == []
    # new forecasts have been created
    assert list(forecast_figures_2) == [employee.basic_pay] * 12
    # non-payroll (other) forecasts were not changed
    assert (
        ForecastMonthlyFigure.objects.filter(financial_code=other_fin_code).count() == 1
    )


def test_is_actual_is_false_for_future_years(db, current_financial_year):
    future_financial_year = FinancialYearFactory(
        financial_year=current_financial_year.financial_year + 1
    )

    apr_period = FinancialPeriod.objects.get(financial_period_code=1)
    apr_period.actual_loaded = True
    apr_period.save()

    current_year_data = get_previous_months_data(current_financial_year)
    future_year_data = get_previous_months_data(future_financial_year)

    for month in current_year_data:
        if month["key"] == "apr":
            assert month["is_actual"] is True
        else:
            assert month["is_actual"] is False

    for month in future_year_data:
        assert month["is_actual"] is False
