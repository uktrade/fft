import os

from django.core.management.base import (
    CommandError,
)

from core.utils.command_helpers import (
    CommandUpload,
)

from end_of_month.upload_archived_month import (
    WrongArchivePeriodException,
)

from forecast.import_csv import WrongChartOFAccountCodeException
from forecast.utils.import_helpers import (
    UploadFileDataError,
    UploadFileFormatError,
)


from previous_years.import_previous_year import upload_previous_year_from_file
from previous_years.utils import (
    ArchiveYearError,
)

from upload_file.models import FileUpload


class Command(CommandUpload):
    help = "Upload a full year of actuals"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        year = options["financial_year"]

        file_name = self.path_to_upload(path, 'xlsx')
        fileobj = FileUpload(
            document_file_name=file_name,
            document_type=FileUpload.PREVIOUSYEAR,
            file_location=FileUpload.LOCALFILE,
        )
        fileobj.save()

        try:
            upload_previous_year_from_file(fileobj, year)
        except (WrongChartOFAccountCodeException,
                WrongArchivePeriodException,
                UploadFileDataError,
                UploadFileFormatError,
                ArchiveYearError
                ) as ex:
            raise CommandError(f"Failure uploading historical actuals: {str(ex)}")
            return

        if self.upload_s3:
            os.remove(file_name)

        self.stdout.write(
            self.style.SUCCESS(
                f"Uploaded historical actuals for year {year}. "
            )
        )
