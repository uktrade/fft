import os

from django.core.management.base import (
    CommandError,
)

from chartofaccountDIT.import_archived_from_csv import (
    import_archived_analysis1,
    import_archived_analysis2,
)

from core.utils.command_helpers import (
    CommandUpload,
)

from forecast.import_csv import WrongChartOFAccountCodeException

from previous_years.utils import (
    ArchiveYearError,
    validate_year_for_archiving,
)


IMPORT_ARCHIVED_TYPE = {
    "Analysis1": import_archived_analysis1,
    "Analysis2": import_archived_analysis2,
}


class Command(CommandUpload):
    help = "Import archived data from csv file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path")
        parser.add_argument("type")
        parser.add_argument("year", type=int)

    # pass the file path as an argument
    # second argument will define the content of the file
    # third argument is the year
    def handle(self, *args, **options):
        path = options.get("csv_path")
        import_type = options.get("type")
        year = options.get("year")
        try:
            validate_year_for_archiving(year)
        except ArchiveYearError as ex:
            raise CommandError(f"Failure import {import_type}: {str(ex)}")

        # TODO Check that the year exists in the database
        file_name = self.path_to_upload(path, 'csv')
        # Windows-1252 or CP-1252, used because of a back quote
        csv_file = open(file_name, newline="", encoding="cp1252")
        try:
            success, msg = IMPORT_ARCHIVED_TYPE[import_type](csv_file, year)
        except WrongChartOFAccountCodeException as ex:
            csv_file.close()
            raise CommandError(f"Failure import {import_type}: {str(ex)}")

        csv_file.close()
        if self.upload_s3:
            os.remove(file_name)
        if success:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully completed import {import_type}.")
            )
        else:
            raise CommandError(f"Failure import {import_type}: {msg}.")
