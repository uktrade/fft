from django.views.generic.base import TemplateView

from download_file.decorators import has_download_permission
from download_file.models import FileDownload


class DownloadView(TemplateView):
    template_name = "download_file/downloaded_files.html"

    @has_download_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadView, self).dispatch(request, *args, **kwargs)

    def downloaded_files(self):
        downloaded_files = FileDownload.objects.all().order_by(
            "-created"
        )

        return downloaded_files
