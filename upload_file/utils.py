from upload_file.models import FileUpload


def set_file_upload_error(file_upload, user_error, error):
    file_upload.status = FileUpload.ERROR
    file_upload.user_error_message = user_error
    file_upload.error_message = error
    file_upload.save()
