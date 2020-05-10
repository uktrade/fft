from django.contrib.auth.decorators import user_passes_test

from download_file.models import FileDownload

from forecast.create_mi_report_source import (create_mi_budget_report,
                                              create_mi_source_report,
                                              )
from forecast.utils.access_helpers import (
    can_download_mi_reports,
)


@user_passes_test(can_download_mi_reports, login_url='index')
def export_mi_report(request):
    file_download = FileDownload(
        downloading_user=request.user,
        document_type=FileDownload.MI_REPORT,
        status=FileDownload.UNPROCESSED
    )
    file_download.save()
    mi_report_source = create_mi_source_report()
    file_download.status = FileDownload.DOWNLOADED
    file_download.save()
    return mi_report_source


@user_passes_test(can_download_mi_reports, login_url='index')
def export_mi_budget_report(request):
    file_download = FileDownload(
        downloading_user=request.user,
        document_type=FileDownload.MI_BUDGET_REPORT,
        status=FileDownload.UNPROCESSED
    )
    file_download.save()
    mi_budget_report_source = create_mi_budget_report()
    file_download.status = FileDownload.DOWNLOADED
    file_download.save()
    return mi_budget_report_source
