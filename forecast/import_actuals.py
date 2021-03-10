import datetime
import logging

from django.db import connection

from core.import_csv import get_fk, get_fk_from_field
from core.models import FinancialYear

from forecast.models import (
    ActualUploadMonthlyFigure,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileFormatError,
    sql_for_data_copy,
    validate_excel_file,
)

from previous_years.utils import (
    CheckArchivedFinancialCode,
)
from previous_years.import_actuals import (
    copy_previous_year_actuals_to_monthly_figure,
)

from previous_years.models import (
    ArchivedActualUploadMonthlyFigure,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

logger = logging.getLogger(__name__)

CHART_OF_ACCOUNT_COL = 3
ACTUAL_FIGURE_COL = 5

TRIAL_BALANCE_FIRST_DATA_ROW = 13

MONTH_CELL = "B2"
TITLE_CELL = "B1"
CORRECT_TRIAL_BALANCE_TITLE = "Detail Trial Balance"
CORRECT_TRIAL_BALANCE_WORKSHEET_NAME = "FNDWRR"

# Sample chart of account entry
# '3000-30000-109189-52191003-310940-00000-00000-0000-0000-0000' # noqa
# The following are the index for the
# chart of account after decoded into a list
CC_INDEX = 2
NAC_INDEX = 3
PROGRAMME_INDEX = 4
ANALYSIS1_INDEX = 5
ANALYSIS2_INDEX = 6
PROJECT_INDEX = 7
CHART_ACCOUNT_SEPARATOR = "-"

# Used when the programme code is 0
GENERIC_PROGRAMME_CODE = 310940


def copy_current_year_actuals_to_monthly_figure(period_obj, financial_year):
    # Now copy the newly uploaded actuals to the monthly figure table
    ForecastMonthlyFigure.objects.filter(
        financial_year=financial_year,
        financial_period=period_obj,
        archived_status__isnull=True,
    ).update(amount=0, starting_amount=0)
    sql_update, sql_insert = sql_for_data_copy(
        FileUpload.ACTUALS,
        period_obj.pk,
        financial_year
    )
    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
        cursor.execute(sql_update)
    ForecastMonthlyFigure.objects.filter(
        financial_year=financial_year,
        financial_period=period_obj,
        amount=0,
        starting_amount=0,
        archived_status__isnull=True,
    ).delete()

    ActualUploadMonthlyFigure.objects.filter(
        financial_year=financial_year, financial_period=period_obj
    ).delete()


def save_trial_balance_row(
    chart_of_account,
        value,
        period_obj,
        year_obj,
        check_financial_code,
        row,
        save_to=ActualUploadMonthlyFigure
):
    """Parse the long strings containing the
    chart of account information. Return errors
    if the elements of the chart of account are missing from database."""

    # Don't save zero values
    if not value:
        return True, ""

    chart_account_list = chart_of_account.split(CHART_ACCOUNT_SEPARATOR)
    programme_code = chart_account_list[PROGRAMME_INDEX]

    # Handle lines without programme code
    if not int(programme_code):
        programme_code = GENERIC_PROGRAMME_CODE

    cost_centre = chart_account_list[CC_INDEX]
    nac = chart_account_list[NAC_INDEX]
    analysis1 = chart_account_list[ANALYSIS1_INDEX]
    analysis2 = chart_account_list[ANALYSIS2_INDEX]
    project_code = chart_account_list[PROJECT_INDEX]
    check_financial_code.validate(
        cost_centre, nac, programme_code, analysis1, analysis2, project_code, row
    )
    if check_financial_code.ignore_row:
        return

    if not check_financial_code.error_found:
        financialcode_obj = check_financial_code.get_financial_code()
        monthlyfigure_obj, created = save_to.objects.get_or_create(
            financial_year=year_obj,
            financial_code=financialcode_obj,
            financial_period=period_obj,
        )
        if created:
            # to avoid problems with precision,
            # we store the figures in pence
            monthlyfigure_obj.amount = value * 100
        else:
            monthlyfigure_obj.amount += value * 100

        monthlyfigure_obj.save()


def check_trial_balance_format(worksheet, calendar_month_number, financial_year):
    """Check that the file is really the trial
    balance and it is the correct month"""

    try:
        if worksheet[TITLE_CELL].value != CORRECT_TRIAL_BALANCE_TITLE:
            raise UploadFileFormatError(
                "This file appears to be corrupt (title is incorrect)"
            )
    except TypeError:
        logger.error(
            "This file appears to be corrupt and it cannot be read",
            exc_info=True
        )
        # wrong file
        raise UploadFileFormatError(
            "This file appears to be corrupt and it cannot be read"
        )

    try:
        report_date = worksheet[MONTH_CELL].value
        if isinstance(report_date, datetime.date):
            report_year = report_date.year
            report_period = report_date.month
        else:
            # If the report is run for an adjustment period,
            # 'worksheet[MONTH_CELL].value' will not contain a date
            # but a string like 'ADJ_3_2019' instead.
            # The fifth character indicates the adjustment period (1, 2 or 3).
            # The last four characters of the string indicate the year.
            # In the forecast period table,
            # the adjustment periods are considered to be
            # after the twelfth month of the financial year,
            # so their value is 13, 14 or 15.
            report_year = int(report_date[-4:])
            report_period = 12 + int(report_date[4:5])

        # The year on the trial balance is the calendar year,
        # and the upload year is the financial year
        # They don't match in Jan, Feb, March
        if calendar_month_number < 4:
            year_to_check = financial_year + 1
        else:
            year_to_check = financial_year

        if report_year != year_to_check:
            # wrong date
            raise UploadFileFormatError("File is for wrong year")
    except TypeError:
        logger.error(
            "This file appears to be corrupt and it cannot be read",
            exc_info=True
        )
        # wrong file
        raise UploadFileFormatError(
            "This file appears to be corrupt and it cannot be read"
        )

    if report_period != calendar_month_number:
        # wrong date
        raise UploadFileFormatError("File is for wrong month/period")

    return True


def validate_trial_balance_report(file_upload, month_number, year):
    try:
        workbook, worksheet = validate_excel_file(
            file_upload,
        )
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        raise ex

    try:
        check_trial_balance_format(worksheet, month_number, year)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    return workbook, worksheet


def upload_trial_balance_report(file_upload, month_number, financial_year):
    workbook, worksheet = validate_trial_balance_report(
        file_upload,
        month_number,
        financial_year)

    year_obj, _ = get_fk(FinancialYear, financial_year)
    period_obj, _ = get_fk_from_field(
        FinancialPeriod, "period_calendar_code", month_number
    )
    if year_obj.current:
        check_financial_code = CheckFinancialCode(file_upload)
        save_to = ActualUploadMonthlyFigure
    else:
        check_financial_code = CheckArchivedFinancialCode(financial_year, file_upload)
        save_to = ArchivedActualUploadMonthlyFigure

    # Clear the table used to upload the actuals.
    # The actuals are uploaded to to a temporary storage, and copied
    # to the MonthlyFigure when the upload is completed successfully.
    # This means that we always have a full upload.
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=financial_year, financial_period=period_obj,
    ).delete()
    rows_to_process = worksheet.max_row + 1
    row = 0

    for actual_row in worksheet.rows:
        row += 1
        if row < TRIAL_BALANCE_FIRST_DATA_ROW:
            # There is no way to start reading rows from a specific place.
            # so keep reading until the first row with data
            continue

        if not row % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                file_upload, f"Processing row {row} of {rows_to_process}."
            )
        chart_of_account = actual_row[CHART_OF_ACCOUNT_COL].value
        if chart_of_account:
            actual = actual_row[ACTUAL_FIGURE_COL].value
            # No need to save 0 values, because the data is cleared
            # before copying the new actuals
            if actual:
                save_trial_balance_row(
                    chart_of_account,
                    actual,
                    period_obj,
                    year_obj,
                    check_financial_code,
                    row,
                    save_to,
                )
        else:
            # needed to avoid processing empty rows at the end of the file
            break
    workbook.close

    final_status = FileUpload.PROCESSED
    if check_financial_code.error_found:
        final_status = FileUpload.PROCESSEDWITHERROR
    else:
        # Now copy the newly uploaded actuals to the correct table
        if year_obj.current:
            copy_current_year_actuals_to_monthly_figure(period_obj, financial_year)
            FinancialPeriod.objects.filter(
                financial_period_code__lte=period_obj.financial_period_code
            ).update(actual_loaded=True)
        else:
            # When uploading data for a previous year, all data is actuals
            # (we cannot forecast for the previous year).
            # Therefore we don't update the actuals flag.
            copy_previous_year_actuals_to_monthly_figure(period_obj, financial_year)

        if check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING

        ActualUploadMonthlyFigure.objects.filter(
            financial_year=financial_year, financial_period=period_obj
        ).delete()

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )
    return True
