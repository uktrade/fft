import os

from django.core.management.base import CommandError

from core.utils.command_helpers import CommandUpload
from previous_years.utils import ArchiveYearError
from treasurySS.import_segment_data_to_archive import (
    WrongHeaderException,
    import_segment_data,
)


# Single use command, needed for patching the archive
class Command(CommandUpload):
    help = "Import historical Treasury segment data from csv file"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        year = options["financial_year"]

        file_name = self.path_to_upload(path, "csv")

        # Windows-1252 or CP-1252, used because of a back quote
        csvfile = open(file_name, newline="", encoding="cp1252")

        try:
            import_segment_data(csvfile, year)
        except (ArchiveYearError, WrongHeaderException) as ex:
            raise CommandError(
                f"Failure uploading historical Treasury segment data: {ex}"
            )
            csvfile.close()
            return

        csvfile.close()
        if self.upload_s3:
            os.remove(file_name)
        self.stdout.write(
            self.style.SUCCESS(
                f"Uploaded historical Treasury segment data for year {year} "
            )
        )
