from upload_file.models import FileUpload


def set_file_upload_error(file_upload, user_error, error):
    file_upload.status = FileUpload.ERROR
    file_upload.user_error_message = "The file is not in the correct format (.xlsx)"
    file_upload.error_message = "BadZipFile (user file is not .xlsx)"
    file_upload.save()
