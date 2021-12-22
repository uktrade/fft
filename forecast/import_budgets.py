from django.db import connection

from core.import_csv import xslx_header_to_dict
from core.models import FinancialYear
from core.utils.generic_helpers import (
    create_financial_year_display,
    get_current_financial_year,
)

from forecast.models import (
    BudgetMonthlyFigure,
    ForecastMonthlyFigure,
    BudgetUploadMonthlyFigure,
    ActualUploadMonthlyFigure,
)
from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileDataError,
    UploadFileFormatError,
    check_header,
    get_month_to_upload,
    sql_for_data_copy,
    validate_excel_file,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

EXPECTED_FIGURE_HEADERS = [
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
    "adj1",
    "adj2",
    "adj3",
]


def copy_uploaded_figures(year, month_dict, upload_type):
    if upload_type == FileUpload.BUDGET:
        target_model =BudgetMonthlyFigure
        uploadmodel = BudgetUploadMonthlyFigure
    else:
        target_model = ForecastMonthlyFigure
        uploadmodel = ActualUploadMonthlyFigure
        
    for period_obj in month_dict.values():
        # Now copy the newly uploaded figures to the monthly figure table
        target_model.objects.filter(
            financial_year=year,
            financial_period=period_obj,
            archived_status__isnull=True,
        ).update(amount=0, starting_amount=0)
        sql_update, sql_insert = sql_for_data_copy(
            upload_type, period_obj.pk, year
        )
        with connection.cursor() as cursor:
            cursor.execute(sql_insert)
            cursor.execute(sql_update)
        target_model.objects.filter(
            financial_year=year,
            financial_period=period_obj,
            amount=0,
            starting_amount=0,
            archived_status__isnull=True,
        ).delete()
    uploadmodel.objects.filter(financial_year=year).delete()


def upload_figures(uploadmodel, data_row, year_obj, financialcode_obj, month_dict):
    for month_idx, period_obj in month_dict.items():
        period_figure = data_row[month_idx].value
        if period_figure is None:
            period_figure = 0
        # We import from Excel, and the user may have entered spaces in an empty cell.
        if type(period_figure) == str:
            period_figure = period_figure.strip()
        if period_figure == '-':
            # we accept the '-' as it is a recognised value in Finance for 0
            period_figure = 0
        try:
            # to avoid problems with precision,
            # we store the figures in pence
            # If period_figure is not a number, it will give a value error
            period_figure = period_figure * 100
        except ValueError:
            raise UploadFileFormatError(
                f"Non-numeric value in {data_row[month_idx].coordinate}:{period_figure}"# noqa
            )
        if period_figure:
            (figure_obj, created,) = uploadmodel.objects.get_or_create(
                financial_year=year_obj,
                financial_code=financialcode_obj,
                financial_period=period_obj,
            )
            if created:
                figure_obj.amount = period_figure
            else:
                figure_obj.amount += period_figure
            figure_obj.save()


def upload_financial_figures(uploadmodel, worksheet, year, header_dict, file_upload):# noqa
    year_obj, created = FinancialYear.objects.get_or_create(financial_year=year)
    if created:
        year_obj.financial_year_display = create_financial_year_display(year)
        year_obj.save()

    include_all_month = (year > get_current_financial_year())

    forecast_months = get_month_to_upload(include_all_month)

    month_dict = {header_dict[k]: v for (k, v) in forecast_months.items()}

    if file_upload.document_type == FileUpload.BUDGET:
        uploadmodel= BudgetUploadMonthlyFigure
    else:
        uploadmodel = ActualUploadMonthlyFigure

    # Clear the table used to upload the figures.
    # They are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    
    uploadmodel.objects.filter(financial_year=year,).delete()
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
    for data_row in worksheet.rows:
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
        cost_centre = data_row[cc_index].value
        if not cost_centre:
            # protection against empty rows
            break
        nac = data_row[nac_index].value
        programme_code = data_row[prog_index].value
        analysis1 = data_row[a1_index].value
        analysis2 = data_row[a2_index].value
        project_code = data_row[proj_index].value
        check_financial_code.validate(
            cost_centre, nac, programme_code,
            analysis1, analysis2, project_code, row_number
        )
        if not check_financial_code.error_found:
            financialcode_obj = check_financial_code.get_financial_code()
            try:
                upload_figures(uploadmodel, data_row, year_obj,
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
        # No errors, so we can copy the figures from the temporary table to the final
        copy_uploaded_figures(year, month_dict)
        if check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )

    return not check_financial_code.error_found


def upload_figure_from_file(file_upload, year, what):
    if file_upload.document_type == FileUpload.BUDGET:
        title = "Budgets"
    else:
        title = "Forecasts"
    try:
        workbook, worksheet = validate_excel_file(file_upload, title)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        raise ex
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_header(header_dict, EXPECTED_FIGURE_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    try:
        upload_financial_figures(worksheet, year, header_dict, file_upload)
    except (UploadFileDataError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    workbook.close


def upload_budget_from_file(file_upload, year):
    upload_figure_from_file(file_upload, year)
