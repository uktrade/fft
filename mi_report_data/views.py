from data_lake.views.utils import FigureFieldData
import csv

from django.db.models import F
from django.http import HttpResponse

from rest_framework.viewsets import ViewSet

from django.db.models import Value, ExpressionWrapper, IntegerField
from django.db.models.functions import Coalesce
from django.views.generic.base import TemplateView

from end_of_month.models import EndOfMonthStatus

from core.utils.generic_helpers import get_current_financial_year

from download_file.decorators import has_download_mi_report_permission

from forecast.models import FinancialPeriod, ForecastMonthlyFigure, BudgetMonthlyFigure

from mi_report_data.models import (
    archived_forecast_actual_view,
    ReportBudgetArchivedData,
    ReportPreviousYearDataView,
)



class DownloadMIDataView(TemplateView):
    template_name = "mi_report_data/download_mi_data.html"

    @has_download_mi_report_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadMIDataView, self).dispatch(request, *args, **kwargs)


class MIReportFieldList:
    filter_on_year = False
    filter_on_archived_period = False
    rename_value_dict = {}
    def list(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={self.filename}.csv"
        writer = csv.writer(response, csv.excel)
        writer.writerow(self.title_list)
        self.write_data(writer)
        return response

    def write_queryset_data(self, writer, qryset):
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
        if self.filter_on_year:
            filter_dict["financial_year_id"]=current_year
        if self.filter_on_archived_period:
            # Download all the archived period.
            max_period_id = (
                EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
            )
            filter_dict["archived_period__lte"] = max_period_id

        market_dict = {market_field: Coalesce(self.market_field, Value("0"))}
        contract_dict = {contract_field: Coalesce(self.contract_field, Value("0"))}
        project_dict = {project_field: Coalesce(self.project_field, Value("0"))}
        forecast_queryset = (
            qryset.select_related(*self.select_related_list)
            .select_related("financial_period", "archived_period")
            .filter(**filter_dict)
            .filter(financial_code__cost_centre__in=[
                "109075",
                "109451",
                "109714",
                "109838"
            ])
            .annotate(
                archiving_year=ExpressionWrapper(
                    Value(current_year), output_field=IntegerField()
                )
            )
            .annotate(**market_dict)
            .annotate(**contract_dict)
            .annotate(**project_dict)
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



class MIReportForecastActualDataSet(ViewSet, FigureFieldData, MIReportFieldList):
    filename = "mi_data_forecast_actual"
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
    data_field_list = [
        "actual",
        "forecast",
    ]

    def write_data(self, writer):
        max_period_id = (
            EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
        )
        for period in range(0, max_period_id):
            self.write_queryset_data(writer, archived_forecast_actual_view[period].objects)
        # Output the current period in two part: first the actuals and after the forecast
        current_year = get_current_financial_year()
        actual_period_id = FinancialPeriod.financial_period_info.actual_month()
        archive_dict = {"archived_status_id": Coalesce("archived_status_id", max_period_id+1)}

        self.rename_value_dict = {"actual":F("amount")}
        current_period_actual_queryset = ForecastMonthlyFigure.objects\
            .filter(archived_status__isnull=True)\
            .filter(financial_year_id=current_year) \
            .annotate(**archive_dict)\
            .annotate(
                forecast=ExpressionWrapper(
                    Value(0), output_field=IntegerField()
                )
            )\
            .filter(financial_period_id__lte=actual_period_id) \
            .annotate(actual=F('amount'))

        self.write_queryset_data(writer, current_period_actual_queryset)




class MIReportBudgetDataSet(ViewSet, FigureFieldData, MIReportFieldList):
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
    filter_on_year = False
    filter_on_archived_period = True

    def write_data(self, writer):
        self.write_queryset_data(writer, ReportBudgetArchivedData)


class MIReportPreviousYearDataSet(ViewSet, FigureFieldData, MIReportFieldList):
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
