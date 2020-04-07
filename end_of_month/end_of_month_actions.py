from django.db import (
    DatabaseError,
    connection,
    transaction,
)
from django.db.models import F, Value, IntegerField

from end_of_month.models import EndOfMonthStatus

from forecast.models import (BudgetMonthlyFigure,
                             FinancialPeriod,
                             ForecastMonthlyFigure,
                             )

from simple_history.utils import bulk_create_with_history

def insert_query(table_name, archived_period_id):
    return f'INSERT INTO public.{table_name}(' \
               f'created, updated, amount, starting_amount, financial_code_id, ' \
               f'financial_period_id, financial_year_id) ' \
               f'SELECT ' \
               f'created, updated, amount, amount, financial_code_id, ' \
               f'financial_period_id, financial_year_id ' \
               f'FROM public.{table_name} ' \
               f'WHERE archived_status_id = {archived_period_id}'


# TODO error handling
def end_of_month_archive(end_of_month_info):
    period_id = end_of_month_info.archived_period.financial_period_code
    # I cannot use transactions because of the direct SQL
    # Add archive period to all the active forecast
    forecast_periods = ForecastMonthlyFigure.objects.filter(
        financial_period__financial_period_code__gt=period_id,
        archived_status__isnull=True)
    forecast_periods.update(archived_status=end_of_month_info)

    # Copy forecast just archived to current forecast
    # Use direct SQL for performance reason.
    # Simple history does not get updated, but it recovers
    #  when changes are done to the record.
    # Note that initial amount is updated to be the current amount.
    forecast_sql = insert_query('forecast_forecastmonthlyfigure',
                                end_of_month_info.archived_period_id)
    with connection.cursor() as cursor:
        cursor.execute(forecast_sql)

    # Archive the budget
    budget_periods = BudgetMonthlyFigure.objects.filter(
        financial_period__financial_period_code__gt=period_id,
        archived_status__isnull=True)
    budget_periods.update(archived_status=end_of_month_info)
    budget_sql =insert_query('forecast_budgetmonthlyfigure',
                             end_of_month_info.archived_period_id)

    with connection.cursor() as cursor:
        cursor.execute(budget_sql)

    # set the archived status to archived
    end_of_month_info.archived = True
    end_of_month_info.save()
