from data_lake.views.data_lake_view import DataLakeViewSet
from data_lake.views.mi_report_views.utils import MIReportFieldList
from data_lake.views.utils import FigureFieldData
from end_of_month.models import EndOfMonthStatus
from mi_report_data.models import (
    ReportCurrentActualData,
    ReportCurrentForecastData,
    archived_forecast_actual_view,
)


BREAK_YEAR_PERIOD = 5


# The view returning the current year data was timing out
# because of the volume of data
# So I split it in two parts, using BREAK_YEAR_PERIOD to split
class MIReportForecastActualBase(DataLakeViewSet, MIReportFieldList):
    forecast_title = [
        "Financial Code ID",
        "Actual",
        "Forecast",
        "Financial Period Code",
        "Financial Period Name",
        "Archived Financial Period Code",
        "Archived Financial Period Name",
        "Year",
        "Archiving Year",
    ]
    title_list = FigureFieldData.chart_of_account_titles.copy()
    title_list.extend(forecast_title)
    data_field_list = ["actual", "forecast"]


class MIReportForecastActual1DataSet(MIReportForecastActualBase):
    filename = "mi_data_forecast_actual_1"

    def write_data(self, writer):
        max_period_id = (
            EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
        )
        # Output the first semester of archived periods.
        # Each db query is derived from the query used to display the yearly
        # data. Not the most efficient way to do it, but it avoids having two ways
        # of extracting the same data
        # Using materialized views to reduce the running time
        for period in range(0, min(BREAK_YEAR_PERIOD, max_period_id + 1)):
            self.write_queryset_data(writer, archived_forecast_actual_view[period])

        # Output the current period in two part:
        # first the actuals and after the forecast
        # The current period in FFT data has Null as archived period
        # For convenience, when sending data to data workspace we change the Null
        # to the next available archived period.
        # It would be better to change the name of the field, but it is late for it!
        self.write_queryset_data(writer, ReportCurrentForecastData)
        self.write_queryset_data(writer, ReportCurrentActualData)


class MIReportForecastActual2DataSet(MIReportForecastActualBase):
    filename = "mi_data_forecast_actual_2"

    def write_data(self, writer):
        max_period_id = (
            EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
        )

        for period in range(BREAK_YEAR_PERIOD, max_period_id + 1):
            self.write_queryset_data(writer, archived_forecast_actual_view[period])
