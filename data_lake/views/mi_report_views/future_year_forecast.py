from data_lake.views.utils import FigureFieldData

from rest_framework.viewsets import ViewSet

from data_lake.views.mi_report_views.utils import (
    ARCHIVED_PERIOD_0_NAME,
    MIReportFieldList,
)

from mi_report_data.models import (
    ReportFutureForecastData,
    ReportFutureForecastPeriod0Data,
)


class MIReportFutureYearForecastDataSet(ViewSet, MIReportFieldList):
    filename = "mi_data_future_year_forecast"
    forecast_title = [
        "Financial Code ID",
        "Future Forecast",
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
        "future_forecast",
    ]

    def write_data(self, writer):
        self.write_queryset_data(writer, ReportFutureForecastData)
        self.write_queryset_data(writer, ReportFutureForecastPeriod0Data)
