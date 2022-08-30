from data_lake.views.utils import FigureFieldData
import csv

from django.http import HttpResponse

from rest_framework.viewsets import ViewSet

from django.db.models import Value, ExpressionWrapper, IntegerField
from django.db.models.functions import Coalesce
from django.views.generic.base import TemplateView

from end_of_month.models import EndOfMonthStatus

from core.utils.generic_helpers import get_current_financial_year

from download_file.decorators import has_download_mi_report_permission

from mi_report_data.models import (
    archived_forecast_actual_view,
    ReportBudgetArchivedData,
    ReportBudgetCurrentData,
    ReportPreviousYearDataView,
    ReportCurrentForecastData,
    ReportCurrentActualData,
)


class DownloadMIDataView(TemplateView):
    template_name = "mi_report_data/download_mi_data.html"

    @has_download_mi_report_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadMIDataView, self).dispatch(request, *args, **kwargs)


class MIReportFieldList(FigureFieldData):
    filter_on_archived_period = False

    def list(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={self.filename}.csv"
        writer = csv.writer(response, csv.excel)
        writer.writerow(self.title_list)
        self.write_data(writer)
        return response

    def write_queryset_data(self, writer, qryset):
        # Apply the filters and annotations common to  the budget, forecast and actual
        # data feed
        #
        current_year = get_current_financial_year()
        self.set_fields()
        # Change the list of fields, to use the field showing 0 instead of null
        market_field = "market"
        contract_field = "contract"
        project_field = "project"
        self.chart_of_account_field_list = [
            self.cost_centre_field,
            self.nac_field,
            self.programme_field,
            contract_field,
            market_field,
            project_field,
            self.expenditure_type_field,
            self.expenditure_type_description_field,
        ]

        filter_dict = {}
        if self.filter_on_archived_period:
            # Download all the archived period.
            max_period_id = (
                EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
            )
            filter_dict["archived_period__lte"] = max_period_id

        annotation_dict = {
            market_field: Coalesce(self.market_field, Value("0")),
            contract_field: Coalesce(self.contract_field, Value("0")),
            project_field: Coalesce(self.project_field, Value("0")),
            "archiving_year": ExpressionWrapper(
                Value(current_year), output_field=IntegerField()
            ),
        }

        forecast_queryset = (
            qryset.objects.select_related(*self.select_related_list)
            .filter(**filter_dict)
            .filter(
                financial_code__cost_centre__cost_centre_code__in=[
                    "109075",
                    "109451",
                    "109714",
                    "109838",
                ]
            )
            .annotate(**annotation_dict)
            .values_list(
                *self.chart_of_account_field_list,
                "financial_code",
                *self.data_field_list,
                "financial_period__financial_period_code",
                "financial_period__period_short_name",
                "archived_period__financial_period_code",
                "archived_period__period_short_name",
                "financial_year_id",
                "archiving_year",
            )
        )
        for row in forecast_queryset:
            writer.writerow(row)


class MIReportForecastActualDataSet(ViewSet, MIReportFieldList):
    filename = "mi_data_forecast_actual"
    forecast_title = [
        "Financial Code ID",
        "Actual",
        "Forecast",
        "Actual Loaded",
        "Financial Period Code",
        "Financial Period Name",
        "Archived Financial Period Code",
        "Archived Financial Period Name",
        "Year",
        "Archiving Year",
    ]
    title_list = FigureFieldData.chart_of_account_titles.copy()
    title_list.extend(forecast_title)
    data_field_list = ["actual", "forecast", "financial_period__actual_loaded"]

    def write_data(self, writer):
        max_period_id = (
            EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
        )
        # Output the archived period.
        # Each db query is derived from the query used to display the yearly
        # data. Not the most efficient way to do it, but it avoids having two ways
        # of extracting the same data
        for period in range(0, max_period_id):
            self.write_queryset_data(writer, archived_forecast_actual_view[period])

        # Output the current period in two part:
        # first the actuals and after the forecast
        # The current period in FFT data has Null as archived period
        # For convenience, when sending data to data workspace we change the Null
        # to the next available archived period.
        # It would be better to change the name of the field, but it is late for it!
        self.write_queryset_data(writer, ReportCurrentForecastData)
        self.write_queryset_data(writer, ReportCurrentActualData)


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


class MIReportPreviousYearDataSet(ViewSet, MIReportFieldList):
    filename = "mi_data_previous_year_actual"
    forecast_title = [
        "Financial Code ID",
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

    def write_data(self, writer):
        self.write_queryset_data(writer, ReportPreviousYearDataView)
