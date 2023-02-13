import logging

from core.utils.generic_helpers import get_current_financial_year
from end_of_month.end_of_month_actions import (
    ArchiveMonthInvalidPeriodError,
    RestoreNonExistingArchiveError,
    get_last_restore_period_id,
)
from end_of_month.models import EndOfMonthStatus, MonthlyTotalBudget
from forecast.models import (
    MAX_PERIOD_CODE,
    BudgetMonthlyFigure,
    FinancialPeriod,
    ForecastMonthlyFigure,
)


logger = logging.getLogger(__name__)


def restore_data(model_name, current_year, period_id):
    # Delete the current data
    model_name.objects.filter(
        financial_year_id=current_year,
        financial_period_id__gte=period_id,
        archived_status__isnull=True,
    ).delete()

    # Delete everything archived in a period later than the one to be restored
    model_name.objects.filter(
        financial_year_id=current_year,
        archived_status__archived_period__financial_period_code__gt=period_id,
    ).delete()

    # Make the data for the period to be restored the current data
    model_name.objects.filter(
        financial_year_id=current_year,
        archived_status__archived_period__financial_period_code=period_id,
    ).update(archived_status=None)


def restore_archive(period_id):
    if period_id > MAX_PERIOD_CODE or period_id < 1:
        error_msg = (
            f"Invalid period {period_id}: "
            f"Valid Period is between 1 and {MAX_PERIOD_CODE}."
        )
        logger.error(error_msg, exc_info=True)
        raise ArchiveMonthInvalidPeriodError(error_msg)

    end_of_month_info = EndOfMonthStatus.objects.get(
        archived_period__financial_period_code=period_id
    )

    if not end_of_month_info.archived:
        error_msg = f"The archive for {period_id} does not exist."
        logger.error(error_msg, exc_info=True)
        raise RestoreNonExistingArchiveError(error_msg)

    current_year = get_current_financial_year()
    restore_data(ForecastMonthlyFigure, current_year, period_id)
    restore_data(BudgetMonthlyFigure, current_year, period_id)

    MonthlyTotalBudget.objects.filter(
        archived_status__archived_period__financial_period_code__gte=period_id,
    ).delete()

    EndOfMonthStatus.objects.filter(
        archived_period__financial_period_code__gte=period_id
    ).update(archived=False, archived_date=None)

    # Clear the actual loaded flag for periods after the se
    FinancialPeriod.objects.filter(financial_period_code__gt=period_id,).update(
        actual_loaded=False,
    )


def restore_last_end_of_month_archive():
    restore_archive(get_last_restore_period_id())
