from django.urls import path

from mi_report_data.views import MIReportDataSet
urlpatterns = [
    path(
        "mi_report_data/",
        MIReportDataSet.as_view({"get": "list"}),
        name="data_lake_mi_report_data",
    ),
]
