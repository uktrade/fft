import logging

from django.db import connection

from end_of_month.models import EndOfMonthStatus

from forecast.models import (
    MAX_PERIOD_CODE,
)

from end_of_month.models import forecast_budget_view_model


logger = logging.getLogger(__name__)


class OutturnInvalidPeriodError(Exception):
    pass


class OuturnNotArchivedMonthError(Exception):
    pass


def validate_period_for_outturn(period_code):
    # Error if period < 1 and > 15
    if period_code > MAX_PERIOD_CODE or period_code < 1:
        error_msg = (
            f"Invalid period {period_code}: "
            f"Valid Period is between 1 and {MAX_PERIOD_CODE}."
        )
        logger.error(error_msg, exc_info=True)
        raise OutturnInvalidPeriodError(error_msg)
    # Error if period not yet archived
    if not EndOfMonthStatus.objects.filter(
        archived_period__financial_period_code=period_code
    ).count():
        error_msg = f'"The selected period {period_code} has not yet been archived."'
        logger.error(error_msg, exc_info=True)
        raise OuturnNotArchivedMonthError(error_msg)


def delete_outturn_for_variance(period_code, year):
    # Use sql for perfomance reasons.
    validate_period_for_outturn(period_code)
    sql_delete = (
        f"DELETE FROM end_of_month_monthlyoutturn "
        f"WHERE outturn_period_id = {period_code}  "
        f"AND financial_year_id = {year}"
    )

    with connection.cursor() as cursor:
        cursor.execute(sql_delete)


def create_outturn_for_variance(period_code, year, used_for_current_month=False):
    validate_period_for_outturn(period_code)

    # Use the database views to create the outturn.
    # It is simpler than calculating from the raw data in monthly_figures
    monthly_data_model = forecast_budget_view_model[period_code]

    db_view_name = monthly_data_model._meta.db_table
    if used_for_current_month:
        use_for_current_data_value = "true"
    else:
        use_for_current_data_value = "false"

    sql_insert = (
        f"INSERT INTO end_of_month_monthlyoutturn("
        f"created,"
        f"updated,"
        f"financial_code_id, "
        f"financial_year_id, "
        f"outturn_period_id, "
        f"next_forecast_period_id, "
        f"previous_outturn, "
        f"used_for_current_month"
        f") "
        f"SELECT "
        f"now(),"
        f"now(),"
        f"financial_code_id, "
        f"financial_year, "
        f"archived_period_id, "
        f"archived_period_id + 1, "
        f"SUM(apr + may + jun + jul + aug + sep + oct + "
        f'nov + "dec" + jan + feb + mar + adj1 + adj2 + adj3), '
        f"{use_for_current_data_value} "
        f"FROM {db_view_name}  "
        f"WHERE financial_year = {year}"
        f"GROUP BY financial_code_id, financial_year, archived_period_id;"
    )

    if used_for_current_month:
        sql_update_current_flag = (
            "UPDATE end_of_month_monthlyoutturn " "SET used_for_current_month = false;"
        )
        with connection.cursor() as cursor:
            cursor.execute(sql_update_current_flag)

    delete_outturn_for_variance(period_code, year)
    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
