import csv
import logging
from decimal import Decimal

from django.db import connection

from core.import_csv import csv_header_to_dict, get_fk
from core.utils.generic_helpers import get_current_financial_year
from end_of_month.models import EndOfMonthStatus
from forecast.import_csv import WrongAmountException, WrongChartOFAccountCodeException
from forecast.models import (
    ActualUploadMonthlyFigure,
    FinancialPeriod,
    FinancialYear,
    ForecastMonthlyFigure,
)
from forecast.utils.import_helpers import CheckFinancialCode
from mi_report_data.utils import refresh_materialised_views


logger = logging.getLogger(__name__)


class WrongArchivePeriodException(Exception):
    pass


def sql_for_single_month_copy(
    financial_period_id,
    archived_period_id,
    financial_year_id,
):
    sql_insert = (
        f"INSERT INTO forecast_forecastmonthlyfigure (created, "
        f"updated, amount, starting_amount, financial_code_id, "
        f"financial_period_id, financial_year_id, archived_status_id) "
        f"SELECT now(), now(), amount, amount, financial_code_id, "
        f"financial_period_id, financial_year_id, {archived_period_id} "
        f"FROM forecast_actualuploadmonthlyfigure "
        f"WHERE "
        f"financial_period_id = {financial_period_id} and "
        f"financial_year_id = {financial_year_id} ; "
    )
    return sql_insert


def import_single_archived_period(  # noqa C901
    csvfile, month_to_upload, archive_period
):
    financial_year = get_current_financial_year()

    # Only forecast is archived each month.
    # Actuals are not archived, because they don't change.
    # As convention, the archive period is identical to the latest
    # actual period. So a period smaller or equal to the archive period
    # indicates a month with actuals.
    if month_to_upload <= archive_period:
        raise WrongArchivePeriodException(
            "You are trying to amend actuals. Only forecast can be amended."
        )

    end_of_month_info = EndOfMonthStatus.objects.get(
        archived_period__financial_period_code=archive_period
    )
    if not end_of_month_info.archived:
        raise WrongArchivePeriodException(
            f"There is no archive for period {archive_period} "
        )

    period_obj = FinancialPeriod.objects.get(pk=month_to_upload)

    archive_period_id = end_of_month_info.id
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=financial_year, financial_period=period_obj
    ).delete()

    reader = csv.reader(csvfile)
    col_key = csv_header_to_dict(next(reader))

    row_number = 1
    fin_obj, msg = get_fk(FinancialYear, financial_year)
    period_obj = FinancialPeriod.objects.get(pk=month_to_upload)

    month_col = col_key[period_obj.period_short_name.lower()]
    check_financial_code = CheckFinancialCode(None)

    csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in csv_reader:
        row_number += 1
        # protection against empty rows
        if len(row) == 0:
            break

        cost_centre = row[col_key["cost centre"]].strip()
        programme_code = row[col_key["programme"]].strip()
        nac = row[col_key["natural account"]].strip()
        analysis1 = row[col_key["analysis"]].strip()
        analysis2 = row[col_key["analysis2"]].strip()
        project_code = row[col_key["project"]].strip()

        check_financial_code.validate(
            cost_centre,
            nac,
            programme_code,
            analysis1,
            analysis2,
            project_code,
            row_number,
        )

        if check_financial_code.error_found or check_financial_code.ignore_row:
            raise WrongChartOFAccountCodeException(
                f"Overwriting period, Row {row_number} error: "
                f"{check_financial_code.display_error}"
            )

        financialcode_obj = check_financial_code.get_financial_code()
        try:
            period_amount = Decimal(row[month_col])
        except (ArithmeticError, IndexError, Decimal.InvalidOperation):
            raise WrongAmountException(
                f"Amount error, Row {row_number} error: "
                f"month_col = {month_col}, val= {row[month_col]}"
            )

        if period_amount:
            month_figure_obj, created = ActualUploadMonthlyFigure.objects.get_or_create(
                financial_year=fin_obj,
                financial_period=period_obj,
                financial_code=financialcode_obj,
            )
            if created:
                month_figure_obj.amount = period_amount * 100
            else:
                month_figure_obj.amount += period_amount * 100
            month_figure_obj.current_amount = month_figure_obj.amount
            month_figure_obj.save()

        if (row_number % 100) == 0:
            logger.info(row_number)

    logger.info(f"Completed processing  {row_number} rows.")
    # Now copy the newly uploaded figures to the monthly figure table
    ForecastMonthlyFigure.objects.filter(
        financial_year=financial_year,
        financial_period=period_obj,
        archived_status_id=archive_period_id,
    ).delete()
    sql_insert = sql_for_single_month_copy(
        month_to_upload, archive_period_id, financial_year
    )
    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
    ForecastMonthlyFigure.objects.filter(
        financial_year=financial_year,
        financial_period=period_obj,
        amount=0,
        starting_amount=0,
        archived_status_id=archive_period_id,
    ).delete()
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=financial_year, financial_period=period_obj
    ).delete()

    # Refresh the views used to send data to data workspace
    refresh_materialised_views()
