from end_of_month.models import (
    EndOfMonthStatus)

from forecast.models import FinancialPeriod


class InvalidPeriodError(Exception):
    pass


class PeriodAlreadyArchivedError(Exception):
    pass


class LaterPeriodAlreadyArchivedError(Exception):
    pass


def user_has_archive_access(user):
    if user.groups.filter(name="Finance Administrator") or user.is_superuser:
        return True


def validate_period_code(period_code, **options):
    period_code = int(period_code)
    if period_code > 15 or period_code < 1:
        raise InvalidPeriodError()
    current_end_of_month_status = EndOfMonthStatus.objects.filter(
        archived_period__financial_period_code=period_code
    ).first()
    if current_end_of_month_status.archived:
        raise PeriodAlreadyArchivedError()
    later_end_of_month_status = EndOfMonthStatus.objects.filter(
        archived=True,
        archived_period__financial_period_code__gt=period_code,
    )
    if later_end_of_month_status.first():
        raise LaterPeriodAlreadyArchivedError()


def get_archivable_month():
    first_month_no_actual = FinancialPeriod.financial_period_info.actual_month() + 1
    if first_month_no_actual > FinancialPeriod.financial_period_info.get_max_period().financial_period_code:  # noqa
        raise InvalidPeriodError()
    is_archived = EndOfMonthStatus.objects.filter(
        archived=True,
        archived_period__financial_period_code=first_month_no_actual,
    ).first()
    if is_archived:
        financial_period = FinancialPeriod.objects.get(
            financial_period_code=first_month_no_actual,
        )
        raise PeriodAlreadyArchivedError(
            f"Period {financial_period.period_long_name} already archived"
        )

    return first_month_no_actual
