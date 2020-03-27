from django.urls import path

from download_file.views.mi_report_download import DownloadMIReportView
from download_file.views.oscar_return import DownloadOscarReturnView

urlpatterns = [
    path(
        "download_oscar_report/",
        DownloadOscarReturnView.as_view(),
        name="download_oscar_report",
    ),
    path(
        "download_mi_report/",
        DownloadMIReportView.as_view(),
        name="download_mi_report"
    ),
]
