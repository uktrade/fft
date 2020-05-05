from upload_file.models import FileUpload


def set_file_upload_fatal_error(file_upload, user_error, error):
    file_upload.status = FileUpload.ERROR
    file_upload.user_error_message = user_error
    file_upload.error_message = error
    file_upload.save()


def set_file_upload_feedback(file_upload, feedback, status=""):
    if status:
        file_upload.status = status
    file_upload.row_process_message = feedback
    file_upload.save()


def set_file_upload_error(file_upload, user_error, error):
    file_upload.status = FileUpload.PARSING
    if file_upload.user_error_message:
        file_upload.error_count += 1
        file_upload.user_error_message = (
            f"{file_upload.user_error_message} {user_error}"
        )
    else:
        file_upload.error_count = 1
        file_upload.user_error_message = user_error
    file_upload.error_message = error
    file_upload.save()


def set_file_upload_warning(file_upload, user_warning):
    if file_upload.user_warning_message:
        file_upload.warning_count += 1
        file_upload.user_warning_message = user_warning
    else:
        file_upload.warning_count = 1
        file_upload.user_warning_message = (
            f"{file_upload.user_warning_message}{user_warning}"
        )
    file_upload.save()


def set_file_upload_finished(file_upload):
    if (
        file_upload.status == FileUpload.PROCESSING
        or file_upload.status == FileUpload.PARSING
    ):
        file_upload.status = FileUpload.PROCESSED
    file_upload.save()
