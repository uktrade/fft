from django.views.generic.base import TemplateView

from download_file.decorators import has_download_oscar_permission
from download_file.models import FileDownload


class DownloadOscarReturnView(TemplateView):
    template_name = "download_file/downloaded_oscar_reports.html"

    @has_download_oscar_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadOscarReturnView, self).dispatch(request, *args, **kwargs)

    def downloaded_files(self):
        downloaded_files = FileDownload.objects.filter(
            document_type=FileDownload.OSCAR_RETURN
        ).order_by("-created")
        return downloaded_files
