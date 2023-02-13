from data_lake.views.utils import FigureFieldData

from rest_framework.viewsets import ViewSet

from data_lake.views.mi_report_views.utils import (
    MIReportFieldList,
)

from mi_report_data.models import (
    ReportPreviousYearDataView,
)


class MIReportPreviousYearDataSet(ViewSet, MIReportFieldList):
    filename = "mi_data_previous_year_actual"
    forecast_title = [
        "Previous Financial Code ID",
        "Previous Year Actual",
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
        "previous_year_actual",
    ]
    exclude_adj_period = False

    def write_data(self, writer):
        self.write_queryset_data(writer, ReportPreviousYearDataView)
