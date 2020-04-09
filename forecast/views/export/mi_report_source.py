from download_file.models import FileDownload

from forecast.create_mi_report_source import create_mi_source_report


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
