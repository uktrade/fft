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

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

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


def copy_actuals_to_monthly_figure(period_obj, year):
    # Now copy the newly uploaded actuals to the monthly figure table
    ForecastMonthlyFigure.objects.filter(
        financial_year=year, financial_period=period_obj,
    ).update(amount=0, starting_amount=0)
    sql_update, sql_insert = sql_for_data_copy(FileUpload.ACTUALS, period_obj.pk, year)
    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
        cursor.execute(sql_update)
    ForecastMonthlyFigure.objects.filter(
        financial_year=year, financial_period=period_obj, amount=0, starting_amount=0
    ).delete()
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=year, financial_period=period_obj
    ).delete()


def save_trial_balance_row(
    chart_of_account, value, period_obj, year_obj, check_financial_code, row
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
        monthlyfigure_obj, created = ActualUploadMonthlyFigure.objects.get_or_create(
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


def check_trial_balance_format(worksheet, period, year):
    """Check that the file is really the trial
    balance and it is the correct period"""

    try:
        if worksheet[TITLE_CELL].value != CORRECT_TRIAL_BALANCE_TITLE:
            raise UploadFileFormatError(
                "This file appears to be corrupt (title is incorrect)"
            )
    except TypeError as ex:
        # wrong file
        raise UploadFileFormatError(
            "This file appears to be corrupt and it cannot be read"
        )

    try:
        report_date = worksheet[MONTH_CELL].value
        if report_date.year != year:
            # wrong date
            raise UploadFileFormatError("File is for wrong year")
    except TypeError as ex:
        # wrong file
        raise UploadFileFormatError(
            "This file appears to be corrupt and it cannot be read"
        )

    if report_date.month != period:
        # wrong date
        raise UploadFileFormatError("File is for wrong period")

    return True


def validate_trial_balance_report(file_upload, month_number, year):
    try:
        workbook, worksheet = validate_excel_file(
            file_upload, CORRECT_TRIAL_BALANCE_WORKSHEET_NAME
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


def upload_trial_balance_report(file_upload, month_number, year):
    workbook, worksheet = validate_trial_balance_report(file_upload, month_number, year)

    year_obj, _ = get_fk(FinancialYear, year)
    period_obj, _ = get_fk_from_field(
        FinancialPeriod, "period_calendar_code", month_number
    )

    # Clear the table used to upload the actuals.
    # The actuals are uploaded to to a temporary storage, and copied
    # to the MonthlyFigure when the upload is completed successfully.
    # This means that we always have a full upload.
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=year, financial_period=period_obj,
    ).delete()
    rows_to_process = worksheet.max_row + 1
    row = 0
    check_financial_code = CheckFinancialCode(file_upload)

    for actual_row in worksheet.rows:
        row += 1
        if row < TRIAL_BALANCE_FIRST_DATA_ROW:
            # There is no way to start reading rows from a specific place.
            # so keep reading until the first row
            continue

        if not row % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                file_upload, f"Processing row {row} of {rows_to_process}."
            )
        chart_of_account = actual_row[CHART_OF_ACCOUNT_COL].value
        if chart_of_account:
            actual = actual_row[ACTUAL_FIGURE_COL].value
            # No need to save 0 values, because the data has been cleared
            # before starting the upload
            if actual:
                save_trial_balance_row(
                    chart_of_account,
                    actual,
                    period_obj,
                    year_obj,
                    check_financial_code,
                    row,
                )
        else:
            break
    workbook.close

    final_status = FileUpload.PROCESSED
    if check_financial_code.error_found:
        final_status = FileUpload.PROCESSEDWITHERROR
    else:
        # Now copy the newly uploaded actuals to the monthly figure table
        copy_actuals_to_monthly_figure(period_obj, year)
        if check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING

        FinancialPeriod.objects.filter(
            financial_period_code__lte=period_obj.financial_period_code
        ).update(actual_loaded=True)

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )
    return True
