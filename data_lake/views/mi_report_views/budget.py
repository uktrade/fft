from rest_framework.viewsets import ViewSet

from data_lake.views.mi_report_views.utils import MIReportFieldList
from data_lake.views.utils import FigureFieldData
from mi_report_data.models import (
    ReportBudgetArchivedData,
    ReportBudgetCurrentData,
    ReportBudgetPeriod0Data,
)


class MIReportBudgetDataSet(ViewSet, MIReportFieldList):
    filename = "mi_data_budget"
    forecast_title = [
        "Financial Code ID",
        "Budget",
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
        "budget",
    ]

    def write_data(self, writer):
        self.filter_on_archived_period = True
        self.write_queryset_data(writer, ReportBudgetArchivedData)
        self.filter_on_archived_period = False
        self.write_queryset_data(writer, ReportBudgetCurrentData)
        self.write_queryset_data(writer, ReportBudgetPeriod0Data)
