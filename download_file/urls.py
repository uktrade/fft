from django.urls import path

from download_file.views.view_oscar_report import (
    UploadedView,
)

urlpatterns = [
    path("files/", UploadedView.as_view(), name="uploaded_files"),
]
