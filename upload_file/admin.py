from django.contrib import admin

from upload_file.models import (
    FileUpload,
    UploadPermission,
)


admin.site.register(FileUpload)
admin.site.register(UploadPermission)
