from django.core.management.base import (
    BaseCommand,
)

from django.core.management.base import (
    CommandError,
)

from end_of_month.upload_archived_month import (
    WrongArchivePeriodException,
)

from forecast.import_csv import WrongChartOFAccountCodeException
from forecast.utils.import_helpers import (
    UploadFileDataError,
    UploadFileFormatError,
)

from previous_years.utils import (
    ArchiveYearError,
)

from previous_years.archive_current_year_figure import archive_current_year


class Command(BaseCommand):
    help = "Archive the figures from the current financial year."

    def handle(self, *args, **options):
        try:
            archive_current_year()
        except (WrongChartOFAccountCodeException,
                WrongArchivePeriodException,
                UploadFileDataError,
                UploadFileFormatError,
                ArchiveYearError
                ) as ex:
            raise CommandError(f"Failure archiving forecast/actual figures: {str(ex)}")
            return

        self.stdout.write(
            self.style.SUCCESS(
                "Current financial year archived. "
            )
        )
