from django.contrib.auth.decorators import user_passes_test

from download_file.models import FileDownload

from forecast.utils.access_helpers import can_download_oscar

from oscar_return.create_oscar_report import (
    create_oscar_report,
    create_previous_year_oscar_report,
)


@user_passes_test(can_download_oscar, login_url="index")
def export_oscar_report(request):
    file_download = FileDownload(
        downloading_user=request.user,
        document_type=FileDownload.OSCAR_RETURN,
        status=FileDownload.UNPROCESSED,
    )
    file_download.save()
    oscar_report = create_oscar_report()
    file_download.status = FileDownload.DOWNLOADED
    file_download.save()
    return oscar_report


@user_passes_test(can_download_oscar, login_url="index")
def export_previous_year_oscar_report(request):
    file_download = FileDownload(
        downloading_user=request.user,
        document_type=FileDownload.OSCAR_RETURN_PREVIOUS_YEAR,
        status=FileDownload.UNPROCESSED,
    )
    file_download.save()
    oscar_report = create_previous_year_oscar_report()
    file_download.status = FileDownload.DOWNLOADED
    file_download.save()
    return oscar_report
