import json
from random import randrange
from statistics import mean

import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.urls import reverse

from chartofaccountDIT.test.factories import ProgrammeCodeFactory
from core.constants import MONTHS
from core.models import FinancialYear
from core.types import MonthsDict
from costcentre.test.factories import CostCentreFactory
from forecast.models import ForecastMonthlyFigure
from forecast.test.factories import FinancialCodeFactory
from payroll.models import EmployeePayPeriods
from payroll.services.payroll import (
    PayrollForecast,
    employee_created,
    payroll_forecast_report,
    update_all_employee_pay_periods,
    update_payroll_forecast,
    update_payroll_forecast_figure,
    vacancy_created,
)

from ..factories import (
    AttritionFactory,
    EmployeeFactory,
    EmployeePayPeriodsFactory,
    FinancialYearFactory,
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
        aug=0.02,
    )
    modifier = 1 + pay_uplift.aug

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
        aug=0.05,
    )
    modifier = 1 - attrition.aug

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
    employee_created(employee)

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


def test_update_all_employee_pay_periods(db):
    # given an employee with pay periods
    EmployeePayPeriodsFactory(year_id=2020)
    # and an employee without pay periods
    EmployeeFactory()

    assert EmployeePayPeriods.objects.count() == 1

    # when `update_all_employee_pay_periods` is called
    update_all_employee_pay_periods()

    # then there are 2 pay periods
    assert EmployeePayPeriods.objects.count() == 2


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
