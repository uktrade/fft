from core.test.factories import FinancialYearFactory
from payroll.services.vacancy import _build_vacancy_pay_periods
from payroll.tests.factories import VacancyFactory


def test_build_vacancy_pay_periods(db):
    # given a vacancy without pay periods
    vacancy = VacancyFactory()
    # and a current financial year
    current_year = FinancialYearFactory(financial_year=2020, current=True)

    # when `build_vacancy_pay_periods` is called for the current year
    current_pay_periods = _build_vacancy_pay_periods(vacancy=vacancy, year=current_year)

    # then we have all false periods
    assert current_pay_periods.periods == [False] * 12
