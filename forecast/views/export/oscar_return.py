from django.contrib.auth.decorators import user_passes_test

from download_file.models import FileDownload

from forecast.create_oscar_report import create_oscar_report
from forecast.utils.access_helpers import (
    can_download_oscar,
)


@user_passes_test(can_download_oscar, login_url='index')
def export_oscar_report(request):
    file_download = FileDownload(
        downloading_user=request.user,
        document_type=FileDownload.OSCAR_RETURN,
        status=FileDownload.UNPROCESSED
    )
    file_download.save()
    oscar_report = create_oscar_report()
    file_download.status = FileDownload.DOWNLOADED
    file_download.save()
    return oscar_report
