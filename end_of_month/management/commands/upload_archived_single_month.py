import os

from django.core.management.base import CommandError

from core.utils.command_helpers import CommandUpload
from end_of_month.upload_archived_month import (
    WrongArchivePeriodException,
    import_single_archived_period,
)
from forecast.import_csv import WrongChartOFAccountCodeException
from forecast.models import MAX_PERIOD_CODE


class Command(CommandUpload):
    help = (
        "Overwrite the forecast for a single period "
        "(1 to 15 starting from April) in a specific archive period."
    )

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument(
            "period_upload",
            type=int,
            help="Period to be uploaded: 1 to 15 starting from April",
        )
        parser.add_argument(
            "archive_period",
            type=int,
            help="Archive period to be updated: 1 to 15 starting from April",
        )

    def handle(self, *args, **options):
        path = options["path"]
        period = options["period_upload"]
        archive_period = options["archive_period"]

        if archive_period > MAX_PERIOD_CODE or archive_period < 1:
            self.stdout.write(
                self.style.ERROR(
                    f"Valid archive Period is between 1 and {MAX_PERIOD_CODE}."
                )
            )
            return
        file_name = self.path_to_upload(path, "csv")

        # Windows-1252 or CP-1252, used because of a back quote
        csvfile = open(file_name, newline="", encoding="cp1252")

        try:
            import_single_archived_period(csvfile, period, archive_period)
        except (WrongChartOFAccountCodeException, WrongArchivePeriodException) as ex:
            raise CommandError(f"Failure uploading forecast period: {str(ex)}")
            csvfile.close()
            return

        csvfile.close()
        if self.upload_s3:
            os.remove(file_name)
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated figures for period {period} "
                f"in archive for period {archive_period}"
            )
        )
