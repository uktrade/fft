from data_lake.views.data_lake_view import DataLakeViewSet
from data_lake.views.mi_report_views.utils import MIReportFieldList
from data_lake.views.utils import FigureFieldData
from mi_report_data.models import ReportFutureBudgetData, ReportFutureBudgetPeriod0Data


class MIReportFutureYearBudgetDataSet(DataLakeViewSet, MIReportFieldList):
    filename = "mi_data_future_year_budget"
    forecast_title = [
        "Financial Code ID",
        "Future budget",
        "Financial Period Code",
        "Financial Period Name",
        "Archived Financial Period Code",
        "Archived Financial Period Name",
        "Year",
        "Archiving Year",
    ]
    title_list = FigureFieldData.chart_of_account_titles.copy()
    title_list.extend(forecast_title)
    data_field_list = [
        "future_budget",
    ]

    def write_data(self, writer):
        self.write_queryset_data(writer, ReportFutureBudgetData)
        self.write_queryset_data(writer, ReportFutureBudgetPeriod0Data)
