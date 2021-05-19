from django.db import connection

from core.utils.generic_helpers import get_current_financial_year

from forecast.models import ForecastMonthlyFigure

from split_project.models import ProjectSplitCoefficient, TemporaryCalculatedValues


class TransferTooLargeError(Exception):
    pass


def copy_values(period_id):
    financial_year_id = get_current_financial_year()
    # clear the previously calculated values
    #  add  the newly calculated values to the current values
    sql_reset_amount = (
        f"UPDATE forecast_forecastmonthlyfigure  "
        f"SET amount=oracle_amount "
        f"WHERE financial_period_id = {period_id} and archived_status_id is null;"
    )
    sql_update = (
        f"UPDATE forecast_forecastmonthlyfigure "
        f"SET amount = amount + c.calculated_amount "
        f"FROM split_project_temporarycalculatedvalues c "
        f"WHERE forecast_forecastmonthlyfigure.financial_period_id = {period_id} "
        f"AND forecast_forecastmonthlyfigure.financial_code_id = c.financial_code_id "
        f"AND archived_status_id is null;"
    )

    sql_insert = (
        f"INSERT INTO forecast_forecastmonthlyfigure "
        f"(created, "
        f"updated, amount, oracle_amount, "
        f"financial_code_id,  "
        f"financial_period_id, financial_year_id) "
        f"SELECT now(), now(),  calculated_amount, 0, "
        f"financial_code_id, "
        f"{period_id}, {financial_year_id} "
        f"FROM split_project_temporarycalculatedvalues "
        f"WHERE "
        f" financial_code_id "
        f"not in (select financial_code_id "
        f"from forecast_forecastmonthlyfigure where "
        f"financial_period_id = {period_id} and "
        f"financial_year_id = {financial_year_id});"
    )

    with connection.cursor() as cursor:
        cursor.execute(sql_reset_amount)
        cursor.execute(sql_update)
        cursor.execute(sql_insert)


def transfer_value(amount, financial_code_id):
    obj = TemporaryCalculatedValues.objects.create(
        financial_code_id=financial_code_id, calculated_amount=amount
    )
    obj.save()


def handle_split_project(financial_period_id):
    # Clear the table used to stored the results while doing the calculations
    TemporaryCalculatedValues.objects.all().delete()
    # First, calculate the new values
    coefficient_queryset = ProjectSplitCoefficient.objects.filter(
        financial_period_id=financial_period_id
    ).order_by("financial_code_from")
    prev_financial_code_from_id = 0
    total_value = 0
    transferred_value = 0
    do_split = False

    for coefficient in coefficient_queryset:
        financial_code_from_id = coefficient.financial_code_from_id
        financial_code_from_obj = coefficient.financial_code_from
        if prev_financial_code_from_id != financial_code_from_id:
            if do_split:
                # complete the transaction we initiated before
                transfer_value(-transferred_value, prev_financial_code_from_id)
            monthly_figure_queryset = ForecastMonthlyFigure.objects.filter(
                financial_period_id=financial_period_id,
                financial_code_id=financial_code_from_id,
            )
            # we cannot transfer money if there is no money in the actuals to be split
            if monthly_figure_queryset.count():
                # Found monthly figure
                do_split = True
                total_value = monthly_figure_queryset.first().oracle_amount
                if total_value == 0:
                    do_split = False
            else:
                do_split = False
            transferred_value = 0
            prev_financial_code_from_id = financial_code_from_id
        if do_split:
            value_to_transfer = (total_value * coefficient.split_coefficient) / 10000
            transferred_value += value_to_transfer
            if transferred_value > total_value:
                # This error should never happen, because the percentages are checked
                # when uploading the data file.
                raise TransferTooLargeError(
                    f"Project split percentage higher that 100% "
                    f"for row f{financial_code_from_obj.human_readable_format()}"
                )
                return

            transfer_value(value_to_transfer, coefficient.financial_code_to_id)

    # processed all the rows, copy the last value
    if do_split:
        transfer_value(-transferred_value, prev_financial_code_from_id)

    # The next  step use raw sql, for speed
    copy_values(financial_period_id)
