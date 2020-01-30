from django.urls import path

from download_file.views.view_oscar_return import (
    DownloadOscarReturnView,
)

urlpatterns = [
    path("download_oscar_report/", DownloadOscarReturnView.as_view(), name="download_oscar_report"),
]
