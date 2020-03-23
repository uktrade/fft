from django.views.generic.base import TemplateView

from download_file.decorators import has_download_mi_report_permission
from download_file.models import FileDownload


class DownloadMIReportView(TemplateView):
    template_name = "download_file/downloaded_mi_reports.html"

    @has_download_mi_report_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadMIReportView, self).dispatch(request, *args, **kwargs)

    def downloaded_files(self):
        downloaded_files = FileDownload.objects.filter(
            document_type=FileDownload.MI_REPORT
        ).order_by("-created")
        return downloaded_files
