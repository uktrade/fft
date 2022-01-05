from django.db.models import Q
from django.views.generic.base import TemplateView

from download_file.decorators import has_download_mi_report_permission
from download_file.models import FileDownload



class YearView(TemplateView):
    table_pagination = False

    def period_form(self):
        return ForecastPeriodForm(selected_period=self.period)


class DownloadMIReportView(TemplateView):
    template_name = "download_file/downloaded_mi_reports.html"

    @has_download_mi_report_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadMIReportView, self).dispatch(request, *args, **kwargs)

    @property
    def financial_year(self):
        return 2022

    def downloaded_files(self):
        downloaded_files = FileDownload.objects.filter(
            Q(document_type=FileDownload.MI_REPORT)
            | Q(document_type=FileDownload.MI_PREVIOUS_YEAR_REPORT)
            | Q(document_type=FileDownload.MI_BUDGET_REPORT)
        ).order_by("-created")
        return downloaded_files
