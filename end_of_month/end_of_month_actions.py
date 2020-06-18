import logging

from django.db import connection
from django.utils import timezone

from end_of_month.models import (EndOfMonthStatus,)

from core.myutils import get_current_financial_year

from forecast.models import (
    BudgetMonthlyFigure,
    ForecastMonthlyFigure,
)

logger = logging.getLogger(__name__)


class ArchiveMonthInvalidPeriodError(Exception):
    pass


class ArchiveMonthAlreadyArchivedError(Exception):
    pass


class ArchiveMonthArchivedPastError(Exception):
    pass


def insert_query(table_name, archived_status_id):
    return (
        f"INSERT INTO public.{table_name}("
        f"created, updated, amount, starting_amount, financial_code_id, "
        f"financial_period_id, financial_year_id) "
        f"SELECT "
        f"created, updated, amount, amount, financial_code_id, "
        f"financial_period_id, financial_year_id "
        f"FROM public.{table_name} "
        f"WHERE archived_status_id = {archived_status_id}"
    )


def insert_total_budget_query(archived_status_id, archived_period_id):
    return (
        f"INSERT INTO public.end_of_month_monthlytotalbudget ("
        f"created, updated, amount, archived_period_id, "
        f"financial_code_id, financial_year_id, archived_status_id)"
        f"SELECT now(), now(), budget, {archived_period_id},"
        f"financial_code_id, financial_year_id, {archived_status_id}"
        f"FROM public.yearly_budget;"
    )


def get_end_of_month(period_code):
    if period_code > 15 or period_code < 1:
        error_msg = f'Invalid period {period_code}: Valid Period is between 1 and 15.'
        logger.error(error_msg, exc_info=True)
        raise ArchiveMonthInvalidPeriodError(error_msg)

    end_of_month_info = EndOfMonthStatus.objects.get(
        archived_period__financial_period_code=period_code
    )
    if end_of_month_info.archived:
        error_msg = f'"The selected period {period_code} has already been archived."'
        logger.error(error_msg, exc_info=True)
        raise ArchiveMonthAlreadyArchivedError(error_msg)

    highest_archived = EndOfMonthStatus.objects.filter(
        archived=True, archived_period__financial_period_code__gt=period_code
    )
    if highest_archived.count():
        error_msg = "A later period has already been archived."
        logger.error(error_msg, exc_info=True)
        raise ArchiveMonthArchivedPastError(error_msg)

    return end_of_month_info


# TODO add transaction
def end_of_month_archive(period_id):
    end_of_month_info = get_end_of_month(period_id)

    current_year = get_current_financial_year()

    # Add archive period to all the active forecast.
    # The actuals are not archived, because they don't change from one month to another
    forecast_periods = ForecastMonthlyFigure.objects.filter(
        financial_period__financial_period_code__gte=period_id,
        financial_year_id=current_year,
        archived_status__isnull=True,
    )
    forecast_periods.update(archived_status=end_of_month_info)

    # Copy forecast just archived to current forecast
    # The current forecast is recognised by  having archive period equal Null.
    # Use direct SQL for performance reason.
    # Simple history does not get updated, but it recovers
    #  when changes are done to the record.
    # Note that initial amount is updated to be the current amount.
    forecast_sql = insert_query("forecast_forecastmonthlyfigure", end_of_month_info.id)
    with connection.cursor() as cursor:
        cursor.execute(forecast_sql)

    # Archive the budget. Use the same logic used for Forecast.
    budget_periods = BudgetMonthlyFigure.objects.filter(
        financial_period__financial_period_code__gte=period_id,
        archived_status__isnull=True,
    )
    budget_periods.update(archived_status=end_of_month_info)
    budget_sql = insert_query("forecast_budgetmonthlyfigure", end_of_month_info.id)

    with connection.cursor() as cursor:
        cursor.execute(budget_sql)

    # Save the yearly total for the budgets. It makes the queries
    # used to display the forecast/budget much easier.
    budget_total_sql = insert_total_budget_query(end_of_month_info.id, period_id)
    with connection.cursor() as cursor:
        cursor.execute(budget_total_sql)

    end_of_month_info.archived = True
    end_of_month_info.archived_date = timezone.now()
    end_of_month_info.save()
