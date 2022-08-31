from django.urls import path

from mi_report_data.views import (
    DownloadMIDataView,
    MIReportForecastActualDataSet,
    MIReportBudgetDataSet,
    MIReportPeriodInUseDataSet,
    MIReportPreviousYearDataSet,
)


urlpatterns = [
    path(
        "data_lake_mi_report_forecast_data/",
        MIReportForecastActualDataSet.as_view({"get": "list"}),
        name="data_lake_mi_report_forecast_data",
    ),
    path(
        "data_lake_mi_report_budget_data/",
        MIReportBudgetDataSet.as_view({"get": "list"}),
        name="data_lake_mi_report_budget_data",
    ),
    path(
        "data_lake_mi_report_previous_year_data/",
        MIReportPreviousYearDataSet.as_view({"get": "list"}),
        name="data_lake_mi_report_previous_year_data",
    ),
    path(
        "data_lake_mi_report_financial_period_in_use/",
        MIReportPeriodInUseDataSet.as_view({"get": "list"}),
        name="data_lake_mi_report_financial_period_in_use",
    ),
    path(
        "download_mi_report_data/",
        DownloadMIDataView.as_view(),
        name="download_mi_report_data",
    ),

]
