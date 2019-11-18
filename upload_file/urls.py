from django.urls import path

from upload_file.views import (
    UploadedView,
)

urlpatterns = [
    path("files/", UploadedView.as_view(), name="uploaded_files"),
]
