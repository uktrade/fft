from django.db import connection

from core.import_csv import xslx_header_to_dict
from core.models import FinancialYear

from forecast.models import (
    BudgetMonthlyFigure,
    BudgetUploadMonthlyFigure,
)
from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileDataError,
    UploadFileFormatError,
    get_forecast_month_dict,
    sql_for_data_copy,
    validate_excel_file,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

EXPECTED_BUDGET_HEADERS = [
    "cost centre",
    "natural account",
    "programme",
    "analysis",
    "analysis2",
    "project",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
    "jan",
    "feb",
    "mar",
]


def check_budget_header(header_dict, correct_header):
    error_msg = ""
    correct = True
    for elem in correct_header:
        if elem not in header_dict:
            correct = False
            error_msg += f"'{elem}' not found. "
    if not correct:
        raise UploadFileFormatError(f"Error in the header: {error_msg}")


def copy_uploaded_budget(year, month_dict):
    for period_obj in month_dict.values():
        # Now copy the newly uploaded budgets to the monthly figure table
        BudgetMonthlyFigure.objects.filter(
            financial_year=year,
            financial_period=period_obj,
            archived_status__isnull=True,
        ).update(amount=0, starting_amount=0)
        sql_update, sql_insert = sql_for_data_copy(
            FileUpload.BUDGET, period_obj.pk, year
        )
        with connection.cursor() as cursor:
            cursor.execute(sql_insert)
            cursor.execute(sql_update)
        BudgetMonthlyFigure.objects.filter(
            financial_year=year,
            financial_period=period_obj,
            amount=0,
            starting_amount=0,
            archived_status__isnull=True,
        ).delete()
    BudgetUploadMonthlyFigure.objects.filter(financial_year=year).delete()


def upload_budget_figures(budget_row, year_obj, financialcode_obj, month_dict):
    for month_idx, period_obj in month_dict.items():
        period_budget = budget_row[month_idx].value
        if period_budget == '-':
            # we accept the '-' as it is a recognised value in Finance for 0
            period_budget = 0
        if not str(period_budget).isnumeric():
            raise UploadFileFormatError(
                f"Non-numeric value in {budget_row[month_idx].coordinate}:{period_budget}"# noqa
            )
        if period_budget:
            (budget_obj, created,) = BudgetUploadMonthlyFigure.objects.get_or_create(
                financial_year=year_obj,
                financial_code=financialcode_obj,
                financial_period=period_obj,
            )
            # to avoid problems with precision,
            # we store the figures in pence
            if created:
                budget_obj.amount = period_budget * 100
            else:
                budget_obj.amount += period_budget * 100
            budget_obj.save()


def upload_budget(worksheet, year, header_dict, file_upload):# noqa
    year_obj, created = FinancialYear.objects.get_or_create(financial_year=year)
    if created:
        year_obj.financial_year_display = f"{year}/{year - 1999}"
        year_obj.save()

    forecast_months = get_forecast_month_dict()
    month_dict = {header_dict[k]: v for (k, v) in forecast_months.items()}
    # Clear the table used to upload the budgets.
    # The budgets are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    BudgetUploadMonthlyFigure.objects.filter(financial_year=year,).delete()
    rows_to_process = worksheet.max_row + 1

    check_financial_code = CheckFinancialCode(file_upload)
    cc_index = header_dict["cost centre"]
    nac_index = header_dict["natural account"]
    prog_index = header_dict["programme"]
    a1_index = header_dict["analysis"]
    a2_index = header_dict["analysis2"]
    proj_index = header_dict["project"]
    row_number = 0
    # There is a terrible performance hit accessing the individual cells:
    # The cell is found starting from cell A0, and continuing until the
    # required cell is found
    # The rows in worksheet.rows are accessed sequentially, so there is no
    # performance problem.
    # A typical files took over 2 hours to read using the cell access method
    # and 10 minutes with the row access.
    for budget_row in worksheet.rows:
        row_number += 1
        if row_number == 1:
            # There is no way to start reading rows from a specific place.
            # Ignore first row, the headers have been processed already
            continue
        if not row_number % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                file_upload, f"Processing row {row_number} of {rows_to_process}."
            )
        cost_centre = budget_row[cc_index].value
        if not cost_centre:
            # protection against empty rows
            break
        nac = budget_row[nac_index].value
        programme_code = budget_row[prog_index].value
        analysis1 = budget_row[a1_index].value
        analysis2 = budget_row[a2_index].value
        project_code = budget_row[proj_index].value
        check_financial_code.validate(
            cost_centre, nac, programme_code,
            analysis1, analysis2, project_code, row_number
        )
        if not check_financial_code.error_found:
            financialcode_obj = check_financial_code.get_financial_code()
            try:
                upload_budget_figures(budget_row, year_obj,
                                      financialcode_obj, month_dict)
            except UploadFileFormatError as ex:
                set_file_upload_fatal_error(
                    file_upload, str(ex), str(ex),
                )
                raise ex

    final_status = FileUpload.PROCESSED
    if check_financial_code.error_found:
        final_status = FileUpload.PROCESSEDWITHERROR
    else:
        # No errors, so we can copy the figures from the temporary table to the budgets
        copy_uploaded_budget(year, month_dict)
        if check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )

    return not check_financial_code.error_found


def upload_budget_from_file(file_upload, year):
    try:
        workbook, worksheet = validate_excel_file(file_upload, "Budgets")
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        raise ex
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_budget_header(header_dict, EXPECTED_BUDGET_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    try:
        upload_budget(worksheet, year, header_dict, file_upload)
    except (UploadFileDataError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    workbook.close
