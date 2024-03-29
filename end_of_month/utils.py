from end_of_month.models import EndOfMonthStatus
from forecast.models import MAX_PERIOD_CODE, FinancialPeriod


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
    if period_code > MAX_PERIOD_CODE or period_code < 1:
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
    last_month_with_actual = FinancialPeriod.financial_period_info.actual_month()
    if not last_month_with_actual:
        raise InvalidPeriodError()
    is_archived = EndOfMonthStatus.objects.filter(
        archived=True,
        archived_period__financial_period_code=last_month_with_actual,
    ).first()
    if is_archived:
        financial_period = FinancialPeriod.objects.get(
            financial_period_code=last_month_with_actual,
        )
        raise PeriodAlreadyArchivedError(
            f"Period {financial_period.period_long_name} already archived"
        )

    return last_month_with_actual


def monthly_variance_exists(period):
    # The monthly variance is not relevant when we display previous or future years
    # or we display the April archived period
    # or there are no archived period (happens in April)
    # period 0 is used for the current period
    if (
        period > 2000
        or period == 1
        or not EndOfMonthStatus.archived_period_objects.archived_list()
    ):
        return False
    else:
        return True
