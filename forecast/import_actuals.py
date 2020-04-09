from django.db import connection

from chartofaccountDIT.models import (
    NaturalCode,
    ProgrammeCode,
)

from core.import_csv import get_fk, get_fk_from_field
from core.models import FinancialYear

from costcentre.models import CostCentre

from forecast.import_utils import (
    UploadFileDataError,
    UploadFileFormatError,
    get_analysys1_obj,
    get_analysys2_obj,
    get_error_from_list,
    get_project_obj,
    sql_for_data_copy,
    validate_excel_file,
)
from forecast.models import (
    ActualUploadMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)

from upload_file.models import FileUpload
from upload_file.utils import set_file_upload_error

CHART_OF_ACCOUNT_COL = "D"
ACTUAL_FIGURE_COL = "F"
NAC_COL = "A"

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

VALID_ECONOMIC_CODE_LIST = ['RESOURCE', 'CAPITAL']

# TODO Read the value from the database. It should be
# possible for the business to change it.
GENERIC_PROGRAMME_CODE = 310940


def copy_actuals_to_monthly_figure(period_obj, year):
    # Now copy the newly uploaded actuals to the monthly figure table
    ForecastMonthlyFigure.objects.filter(
        financial_year=year,
        financial_period=period_obj,
    ).update(amount=0, starting_amount=0)
    sql_update, sql_insert = sql_for_data_copy(FileUpload.ACTUALS, period_obj.pk, year)
    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
        cursor.execute(sql_update)
    ForecastMonthlyFigure.objects.filter(
        financial_year=year,
        financial_period=period_obj,
        amount=0,
        starting_amount=0
    ).delete()
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=year,
        financial_period=period_obj
    ).delete()


def save_trial_balance_row(chart_of_account, value, period_obj, year_obj):
    """Parse the long strings containing the
    chart of account information. Return errors
    if the elements of the chart of account are missing from database."""
    chart_account_list = chart_of_account.split(CHART_ACCOUNT_SEPARATOR)
    programme_code = chart_account_list[PROGRAMME_INDEX]
    # TODO put GENERIC_PROGRAMME_CODE in database
    # Handle lines without programme code
    if not int(programme_code):
        if value:
            programme_code = GENERIC_PROGRAMME_CODE
        else:
            return True, ""
    cost_centre = chart_account_list[CC_INDEX]
    nac = chart_account_list[NAC_INDEX]
    analysis1 = chart_account_list[ANALYSIS1_INDEX]
    analysis2 = chart_account_list[ANALYSIS2_INDEX]
    project_code = chart_account_list[PROJECT_INDEX]

    error_list = []
    nac_obj, message = get_fk(NaturalCode, nac)
    error_list.append(message)
    if nac_obj:
        #  Check that the NAC is resource or capital
        if not nac_obj.economic_budget_code or \
                nac_obj.economic_budget_code.upper() not in VALID_ECONOMIC_CODE_LIST:
            return True, ""
    cc_obj, message = get_fk(CostCentre, cost_centre)
    error_list.append(message)
    programme_obj, message = get_fk(ProgrammeCode, programme_code)
    error_list.append(message)
    analysis1_obj, message = get_analysys1_obj(analysis1)
    error_list.append(message)
    analysis2_obj, message = get_analysys2_obj(analysis2)
    error_list.append(message)
    project_obj, message = get_project_obj(project_code)
    error_list.append(message)
    error_message = get_error_from_list(error_list)
    if error_message:
        raise UploadFileDataError(
            error_message
        )
    financialcode_obj, created = FinancialCode.objects.get_or_create(
        programme=programme_obj,
        cost_centre=cc_obj,
        natural_account_code=nac_obj,
        analysis1_code=analysis1_obj,
        analysis2_code=analysis2_obj,
        project_code=project_obj,
    )
    financialcode_obj.save()
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
    return True


def check_trial_balance_format(worksheet, period, year):
    """Check that the file is really the trial
    balance and it is the correct period"""

    if worksheet[TITLE_CELL].value != CORRECT_TRIAL_BALANCE_TITLE:
        # wrong file
        raise UploadFileFormatError(
            "This file appears to be corrupt (title is incorrect)"
        )

    report_date = worksheet[MONTH_CELL].value
    if report_date.year != year:
        # wrong date
        raise UploadFileFormatError(
            "File is for wrong year"
        )

    if report_date.month != period:
        # wrong date
        raise UploadFileFormatError(
            "File is for wrong period"
        )

    return True


def upload_trial_balance_report(file_upload, month_number, year):
    try:
        workbook, worksheet = \
            validate_excel_file(file_upload, CORRECT_TRIAL_BALANCE_WORKSHEET_NAME)
    except UploadFileFormatError as ex:
        set_file_upload_error(
            file_upload,
            str(ex),
            str(ex),
        )
        raise ex

    try:
        check_trial_balance_format(worksheet, month_number, year)
    except UploadFileFormatError as ex:
        set_file_upload_error(
            file_upload,
            str(ex),
            str(ex),
        )
        workbook.close
        raise ex

    year_obj, msg = get_fk(FinancialYear, year)
    period_obj, msg = get_fk_from_field(
        FinancialPeriod,
        "period_calendar_code",
        month_number)

    # Clear the table used to upload the actuals.
    # The actuals are uploaded to to a temporary storage, and copied
    # to the MonthlyFigure when the upload is completed successfully.
    # This means that we always have a full upload.
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=year,
        financial_period=period_obj,
    ).delete()

    for row in range(TRIAL_BALANCE_FIRST_DATA_ROW, worksheet.max_row + 1):
        # don't delete this comment: useful for debugging, but it gives a
        # 'too complex error'
        # if not row % 100:
        #     print(row)
        chart_of_account = worksheet["{}{}".format(CHART_OF_ACCOUNT_COL, row)].value
        if chart_of_account:
            actual = worksheet["{}{}".format(ACTUAL_FIGURE_COL, row)].value
            # No need to save 0 values, because the data has been cleared
            # before starting the upload
            if actual:
                try:
                    save_trial_balance_row(chart_of_account,
                                           actual,
                                           period_obj,
                                           year_obj)
                except UploadFileDataError as ex:
                    workbook.close
                    msg = 'Error at row {}: {}'. \
                        format(row, str(ex))
                    set_file_upload_error(
                        file_upload,
                        msg,
                        msg,
                    )
                    raise ex
        else:
            break

    # Now copy the newly uploaded actuals to the monthly figure table
    copy_actuals_to_monthly_figure(period_obj, year)
    period_obj.actual_loaded = True
    # TODO set all previous month to be Actual Loaded
    period_obj.save()
    workbook.close
    return True
