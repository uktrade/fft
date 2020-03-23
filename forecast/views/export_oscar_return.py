from download_file.models import FileDownload

from forecast.create_oscar_report import create_oscar_report


def export_oscar_report(request):
    file_download = FileDownload(
        downloading_user=request.user,
        document_type=FileDownload.OSCAR_RETURN,
        status=FileDownload.UNPROCESSED
    )
    file_download.save()
    oscar_report = create_oscar_report()
    file_download.status = FileDownload.DOWNLOADED
    return oscar_report
