from django.db.models import Q

from download_file.decorators import has_download_mi_report_permission
from download_file.forms import DownloadMIForm
from download_file.models import FileDownload

from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormView

from core.utils.generic_helpers import get_current_financial_year, get_year_display


class DownloadMIReportView(FormView):
    template_name = "download_file/downloaded_mi_reports.html"
    form_class = DownloadMIForm

    @has_download_mi_report_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadMIReportView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.financial_year = request.POST.get("download_year", None,)

        if request.POST.get("download_budget_name", None,):
            url_name = "download_mi_budget"
        else:
            url_name = "download_mi_report_source"

        return HttpResponseRedirect(
            reverse(url_name, kwargs={"financial_year": self.financial_year})
        )

    def downloaded_files(self):
        downloaded_files = FileDownload.objects.filter(
            Q(document_type=FileDownload.MI_REPORT)
            | Q(document_type=FileDownload.MI_PREVIOUS_YEAR_REPORT)
            | Q(document_type=FileDownload.MI_BUDGET_REPORT)
        ).order_by("-created")
        return downloaded_files

    def previous_year(self):
        return get_year_display(get_current_financial_year() - 1)
