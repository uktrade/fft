from data_lake.views.utils import FigureFieldData
import csv

from core.utils.generic_helpers import get_current_financial_year

from django.http import HttpResponse

from rest_framework.viewsets import ViewSet

from mi_report_data.models import ReportDataView

from django.views.generic.base import TemplateView

from download_file.decorators import has_download_mi_report_permission

from end_of_month.models import EndOfMonthStatus

class DownloadMIDataView(TemplateView):
    template_name = "mi_report_data/download_mi_data.html"

    @has_download_mi_report_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadMIDataView, self).dispatch(request, *args, **kwargs)


class MIReportDataSet(ViewSet, FigureFieldData):
    filename = "mi_data"
    forecast_title = [
        "Budget",
        "Actual",
        "Forecast",
        "Financial Period Code",
        "Financial Period Name",
        "Archived Financial Period Code",
        "Archived Financial Period Name",
        "Year",
    ]
    title_list = FigureFieldData.chart_of_account_titles.copy()
    title_list.extend(forecast_title)

    def list(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={self.filename}.csv"
        writer = csv.writer(response, csv.excel)
        writer.writerow(self.title_list)
        self.write_data(writer)
        return response

    def write_data(self, writer):
        current_year = get_current_financial_year()
        self.set_fields()
        # Download all the archived period, plus 1.
        # The plus 1 is the current period.
        max_period_id = (
            EndOfMonthStatus.archived_period_objects.get_latest_archived_period() + 1
        )
        forecast_queryset = (
            ReportDataView.objects
            .select_related(*self.select_related_list)
            .select_related("financial_period", "archived_period")
            .filter(financial_year_id=current_year)
            .filter(archived_period_id__lte=max_period_id)
            .values_list(
                *self.chart_of_account_field_list,
                "budget",
                "actual",
                "forecast",
                "financial_period__financial_period_code",
                "financial_period__period_short_name",
                "archived_period__financial_period_code",
                "archived_period__period_short_name",
                "financial_year_id",
            )
        )

        for row in forecast_queryset:
            writer.writerow(row)
