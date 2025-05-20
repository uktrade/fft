from core.models import FinancialYear
from payroll.models import Vacancy, VacancyPayPeriods
from payroll.services.payroll import update_payroll_forecast


def vacancy_created(vacancy: Vacancy) -> None:
    """Hook to be called after a vacancy instance is created."""
    # Create VacancyPayPeriods records for current and future financial years.
    for year in FinancialYear.objects.forecast():
        _build_vacancy_pay_periods(vacancy=vacancy, year=year).save()

    # There is no need to update the payroll forecast here. This is because a vacancy is
    # created with no pay periods enabled and therefore has no impact on the forecast.
    return


def vacancy_updated(vacancy: Vacancy) -> None:
    """Hook to be called after a vacancy instance is updated."""
    update_payroll_forecast(cost_centre=vacancy.cost_centre)


def vacancy_deleted(vacancy: Vacancy) -> None:
    """Hook to be called after a vacancy instance is deleted."""
    update_payroll_forecast(cost_centre=vacancy.cost_centre)


def _build_vacancy_pay_periods(
    *, vacancy: Vacancy, year: FinancialYear
) -> VacancyPayPeriods:
    obj = VacancyPayPeriods(vacancy=vacancy, year=year)
    obj.periods = [False] * 12

    return obj
