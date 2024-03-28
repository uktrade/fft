from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from guardian.shortcuts import get_objects_for_user, remove_perm

from core.import_csv import xslx_header_to_dict
from forecast.utils.import_helpers import (
    UploadFileFormatError,
    check_header,
    validate_excel_file,
)
from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
    set_file_upload_warning,
)


EXPECTED_USER_HEADERS = [
    "first name",  # /PS-IGNORE
    "last name",  # /PS-IGNORE
]

PERMISSION = "costcentre.change_costcentre"

UserModel = get_user_model()


class UserNotFoundError(Exception):
    pass


def delete_user(first_name: str, last_name: str) -> str:
    user_queryset = UserModel.objects.filter(first_name=first_name, last_name=last_name)
    message = f"User {first_name} {last_name} deleted."
    if user_queryset.count() == 0:
        raise UserNotFoundError(f"User {first_name} {last_name} not found.")

    if user_queryset.count() > 1:
        # warning,  multiple users with same email
        message = f"{user_queryset.count} users named {first_name} {last_name} deleted."
    # Remove access to cost centres
    for user_obj in user_queryset:
        cost_centre_list = get_objects_for_user(user_obj, PERMISSION)
        for cost_centre in cost_centre_list:
            remove_perm(PERMISSION, user_obj, cost_centre)

        user_obj.groups.clear()
        user_obj.user_permissions.clear()
        if not user_obj.username:
            # A user may not have a username defined,
            # but without a username you cannot save the user.
            # Generate a random string to fill the username
            user_obj.username = get_random_string(length=32)
        user_obj.is_superuser = False
        user_obj.is_staff = False
        # The user is not removed from the database, it is made non active
        user_obj.is_active = False
        user_obj.save()
    return message


def validate_user_file(file_upload: FileUpload):
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


def bulk_delete_users(file_obj: FileUpload) -> int:
    workbook, worksheet = validate_user_file(file_obj)

    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_header(header_dict, EXPECTED_USER_HEADERS)
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
    user_first_name_index = header_dict["first name"]  # /PS-IGNORE
    user_last_name_index = header_dict["last name"]  # /PS-IGNORE
    error_found = False
    for user_row in worksheet.rows:
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
        first_name = user_row[user_first_name_index].value
        last_name = user_row[user_last_name_index].value
        if last_name:
            try:
                message = delete_user(first_name, last_name)
                set_file_upload_warning(file_obj, message)
            except UserNotFoundError as ex:

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
    workbook.close()

    final_status = FileUpload.PROCESSED
    if error_found:
        final_status = FileUpload.PROCESSEDWITHERROR

    set_file_upload_feedback(
        file_obj, f"Processed {rows_to_process} rows.", final_status
    )
    return rows_to_process
