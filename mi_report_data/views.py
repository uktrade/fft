from data_lake.views.utils import FigureFieldData
import csv

from core.utils.generic_helpers import get_current_financial_year

from django.http import HttpResponse

from rest_framework.viewsets import ViewSet

from mi_report_data.models import ReportDataView

from django.db.models import Value, ExpressionWrapper, IntegerField
from django.db.models.functions import Coalesce
from django.views.generic.base import TemplateView

from download_file.decorators import has_download_mi_report_permission

from end_of_month.models import EndOfMonthStatus


class DownloadMIDataView(TemplateView):
    template_name = "mi_report_data/download_mi_data.html"

    @has_download_mi_report_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadMIDataView, self).dispatch(request, *args, **kwargs)


class MIReportFieldList:
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
        # Download all the archived period, plus 1.
        # The plus 1 is the current period.
        max_period_id = (
            EndOfMonthStatus.archived_period_objects.get_latest_archived_period() + 1
        )
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

        market_dict = {market_field: Coalesce(self.market_field, Value("0"))}
        contract_dict = {contract_field: Coalesce(self.contract_field, Value("0"))}
        project_dict = {project_field: Coalesce(self.project_field, Value("0"))}
        forecast_queryset = (
            qryset.objects.select_related(*self.select_related_list)
            .select_related("financial_period", "archived_period")
            .filter(financial_year_id=current_year)
            .filter(financial_code__cost_centre__in=[
                "109075",
                "109451",
                "109714",
                "109838"
            ])
            .filter(archived_period_id__lte=max_period_id)
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


class MIReportDataSet(ViewSet, FigureFieldData, MIReportFieldList):
    filename = "mi_data"
    forecast_title = [
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
        return self.write_queryset_data(writer, ReportDataView)
