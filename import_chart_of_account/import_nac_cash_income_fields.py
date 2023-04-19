from django.db import IntegrityError, connection

from chartofaccountDIT.models import NaturalCode
from core.import_csv import xslx_header_to_dict
from forecast.utils.import_helpers import (
    UploadFileFormatError,
    check_header,
    validate_excel_file,
)
from import_chart_of_account.models import UploadNaturalCode
from upload_file.models import FileUpload
from upload_file.utils import set_file_upload_fatal_error, set_file_upload_feedback


NAC_HEADER = "natural account code"  # /PS-IGNORE
CASH_HEADER = "cash non_cash"  # /PS-IGNORE
INCOME_HEADER = "gross income"  # /PS-IGNORE

EXPECTED_NAC_HEADERS = [
    NAC_HEADER,
    INCOME_HEADER,
    CASH_HEADER,
]

# Use the choice field values to validate entries.
gross_income_values = {
    v.lower(): k for k, v in dict(NaturalCode.GROSS_INCOME_CHOICE).items()
}
cash_non_cash_values = {
    v.lower(): k for k, v in dict(NaturalCode.CASH_NONCASH_CHOICE).items()
}


def validate_uploaded_file(file_upload: FileUpload):
    try:
        workbook, worksheet = validate_excel_file(
            file_upload,
        )
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload,
            str(ex),
            str(ex),
        )
        raise ex
    return workbook, worksheet


def update_with_sql():
    current_sql = (
        'UPDATE "chartofaccountDIT_naturalcode" '
        "SET cash_non_cash=imp.cash_non_cash, gross_income=imp.gross_income "
        "FROM import_chart_of_account_uploadnaturalcode imp "
        "WHERE imp.natural_account_code "
        ' = "chartofaccountDIT_naturalcode".natural_account_code;'
    )

    archived_sql = (
        'UPDATE "chartofaccountDIT_archivednaturalcode" '
        "SET cash_non_cash=imp.cash_non_cash, gross_income=imp.gross_income "
        "FROM import_chart_of_account_uploadnaturalcode imp "
        "WHERE imp.natural_account_code  "
        ' = "chartofaccountDIT_archivednaturalcode".natural_account_code;'
    )

    with connection.cursor() as cursor:
        cursor.execute(current_sql)
        cursor.execute(archived_sql)


def upload_nac_fields(file_obj: FileUpload) -> int:  # noqa C901
    workbook, worksheet = validate_uploaded_file(file_obj)

    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_header(header_dict, EXPECTED_NAC_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_obj,
            str(ex),
            str(ex),
        )

    file_obj.status = FileUpload.PROCESSING
    file_obj.save()
    rows_to_process = worksheet.max_row + 1
    row_count = 0
    gross_income_index = header_dict[INCOME_HEADER]
    cash_non_cash_index = header_dict[CASH_HEADER]
    nac_index = header_dict[NAC_HEADER]

    error_found = False
    UploadNaturalCode.objects.all().delete()
    for nac_row in worksheet.rows:
        add_row = True
        row_count += 1
        if row_count < 2:
            # There is no way to start reading rows from a specific place.
            # so keep reading until the first row with data
            continue
        if row_count % 100 == 0:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                file_obj, f"Processing row {row_count} of {rows_to_process}."
            )
        nac_value = nac_row[nac_index].value
        if nac_value:
            gross_income = nac_row[gross_income_index].value
            cash_non_cash = nac_row[cash_non_cash_index].value
            if gross_income == "" or cash_non_cash == "":
                error_message = f"Row {row_count}: Empty values not allowed."
                set_file_upload_fatal_error(
                    file_obj,
                    error_message,
                    "",
                )
                error_found = True
                add_row = False
            else:
                try:
                    gross_income_value = gross_income_values[gross_income.lower()]
                except KeyError as ex:
                    error_found = True
                    add_row = False
                    error_message = f"Row {row_count}: {gross_income} " \
                                    f"not a valid value for 'Gross/Income'"
                    set_file_upload_fatal_error(
                        file_obj,
                        error_message,
                        str(ex),
                    )
                try:
                    cash_non_cash_value = cash_non_cash_values[cash_non_cash.lower()]
                except KeyError as ex:
                    error_found = True
                    add_row = False
                    error_message = f"Row {row_count}: {cash_non_cash} " \
                                    f"not a valid value for 'Cash/Non Cash'"
                    set_file_upload_fatal_error(
                        file_obj,
                        error_message,
                        str(ex),
                    )

            if add_row:
                try:
                    UploadNaturalCode.objects.create(
                        natural_account_code=nac_value,
                        gross_income=gross_income_value,
                        cash_non_cash=cash_non_cash_value,
                    )
                except IntegrityError as ex:
                    error_found = True
                    error_message = f"Row {row_count}: {str(ex)}"
                    set_file_upload_fatal_error(
                        file_obj,
                        error_message,
                        str(ex),
                    )
        else:
            # needed to avoid processing empty rows at the end of the file
            break
    workbook.close

    if not error_found:
        # copy new fields to tables. Use direct sql for performance
        update_with_sql()
        final_status = FileUpload.PROCESSED
        final_message = f"Processed {rows_to_process} rows."
        success = True

    if error_found:
        final_status = FileUpload.PROCESSEDWITHERROR
        final_message = f"Processed {rows_to_process} rows with errors. " \
                        f"{file_obj.user_error_message}"
        success = False

    set_file_upload_feedback(
        file_obj, f"Processed {rows_to_process} rows.", final_status
    )
    file_obj.user_error_message
    return final_message, success
