from statistics import mean

import pytest

from core.constants import MONTHS
from chartofaccountDIT.test.factories import ProgrammeCodeFactory
from core.models import FinancialYear
from costcentre.test.factories import CostCentreFactory
from forecast.models import ForecastMonthlyFigure
from payroll.services.payroll import (
    employee_created,
    payroll_forecast_report,
    vacancy_created,
    PayrollForecast,
    update_forecast,
)
from forecast.test.factories import FinancialCodeFactory

from ..factories import (
    AttritionFactory,
    EmployeeFactory,
    PayUpliftFactory,
    VacancyFactory,
)


# NOTE: These must match the PAYROLL.BASIC_PAY_NAC, PAYROLL.PENSION_NAC and PAYROLL.ERNIC_NAC settings.
SALARY_NAC = "71111001"
PENSION_NAC = "71111002"
ERNIC_NAC = "71111003"
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
                expected_result = pension
            else:
                expected_result = ernic

            assert float(report[nac][month]) == pytest.approx(expected_result)


def test_payroll_forecast(db):
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


def test_one_employee_with_no_modifiers(db):
    cost_centre = CostCentreFactory.create(cost_centre_code="123456")

    payroll_employee_1 = EmployeeFactory.create(
        cost_centre=cost_centre,
        basic_pay=195000,
        pension=7550,
        ernic=2000,
    )

    employee_created(payroll_employee_1)

    financial_year = FinancialYear.objects.current()

    report = payroll_forecast_report(cost_centre, financial_year)

    report_by_nac = {x["natural_account_code"]: x for x in report}

    e1s = ((2000 - 100) + (100 - 50)) * 100
    e1p = (75.5 - 0) * 100
    e1e = payroll_employee_1.ernic

    assert_report_results_with_modifiers(report_by_nac, e1s, e1p, e1e)


def test_one_employee_with_pay_uplift(db):
    cost_centre = CostCentreFactory.create(cost_centre_code="123456")

    payroll_employee_1 = EmployeeFactory.create(
        cost_centre=cost_centre,
        basic_pay=195000,
        pension=7550,
        ernic=2000,
    )

    employee_created(payroll_employee_1)

    financial_year = FinancialYear.objects.current()

    pay_uplift = PayUpliftFactory.create(
        financial_year=financial_year,
        aug=1.02,
    )
    modifier = pay_uplift.aug

    report = payroll_forecast_report(cost_centre, financial_year)

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


def test_one_employee_with_attrition(db):
    cost_centre = CostCentreFactory.create(cost_centre_code="123456")

    payroll_employee_1 = EmployeeFactory.create(
        cost_centre=cost_centre,
        basic_pay=195000,
        pension=7550,
        ernic=2000,
    )

    employee_created(payroll_employee_1)

    financial_year = FinancialYear.objects.current()

    attrition = AttritionFactory.create(
        cost_centre=cost_centre,
        financial_year=financial_year,
        aug=0.95,
    )
    modifier = attrition.aug

    report = payroll_forecast_report(cost_centre, financial_year)

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


def test_scenario_update_forecast():
    cost_centre = CostCentreFactory.create(cost_centre_code="123456")
    programme_code = ProgrammeCodeFactory.create()

    financial_code_salary = FinancialCodeFactory(
        cost_centre=cost_centre,
        programme_code=programme_code,
        natural_account_code__natural_account_code="71111001",
    )
    financial_code_pension = FinancialCodeFactory(
        cost_centre=cost_centre,
        programme_code=programme_code,
        natural_account_code__natural_account_code="71111002",
    )
    financial_code_ernic = FinancialCodeFactory(
        cost_centre=cost_centre,
        programme_code=programme_code,
        natural_account_code__natural_account_code="71111003",
    )

    financial_year = FinancialYear.objects.current()

    payroll_forecast = [
        PayrollForecast(
            programme_code=programme_code,
            natural_account_code="71111001",
            apr=1,
            may=1,
            jun=1,
            jul=1,
            aug=1,
            sep=1,
            oct=1,
            dec=1,
            jan=1,
            feb=1,
            mar=1,
        )
    ]

    update_forecast(
        financial_year=financial_year,
        cost_centre=cost_centre,
        payroll_forecast=payroll_forecast,
    )

    assert (
        ForecastMonthlyFigure.objects.get(
            financial_year=financial_year,
            financial_period__financial_period_code=1,
            financial_code=financial_code_salary,
        )
        == 1
    )
