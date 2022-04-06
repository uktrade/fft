from django.urls import path

from mi_report_data.views import DownloadMIDataView, MIReportDataSet

urlpatterns = [
    path(
        "data_lake_mi_report_data/",
        MIReportDataSet.as_view({"get": "list"}),
        name="data_lake_mi_report_data",
    ),
    path(
        "download_mi_report_data/",
        DownloadMIDataView.as_view(),
        name="download_mi_report_data",
    ),

]
