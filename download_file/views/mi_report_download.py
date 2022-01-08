from django.db.models import Q
from django.views.generic.base import TemplateView

from core.utils.generic_helpers import get_current_financial_year
from download_file.decorators import has_download_mi_report_permission
from download_file.forms import DownloadMIForm
from download_file.models import FileDownload



import logging

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


logger = logging.getLogger(__name__)



class DownloadMIReportView(TemplateView):
    template_name = "download_file/downloaded_mi_reports.html"

    def year_form(self):
        return DownloadMIForm(selected_year=self.financial_year)

    @has_download_mi_report_permission
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadMIReportView, self).dispatch(request, *args, **kwargs)

    @property
    def financial_year(self):
        return get_current_financial_year()

    def downloaded_files(self):
        downloaded_files = FileDownload.objects.filter(
            Q(document_type=FileDownload.MI_REPORT)
            | Q(document_type=FileDownload.MI_PREVIOUS_YEAR_REPORT)
            | Q(document_type=FileDownload.MI_BUDGET_REPORT)
        ).order_by("-created")
        return downloaded_files
