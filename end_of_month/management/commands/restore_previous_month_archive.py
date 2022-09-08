from django.core.management.base import BaseCommand

from end_of_month.restore_archive import (
    restore_archive,
    restore_last_end_of_month_archive,
)
from forecast.models import MAX_PERIOD_CODE


class Command(BaseCommand):
    help = (
        "Restore archived forecast and budget to be the current one: "
        "1 to 15 starting from April. 0 will restore the latest archive."
        "Beware: it will overwrite the current forecast!"
    )

    def add_arguments(self, parser):
        parser.add_argument("period", type=int)

    def handle(self, *args, **options):
        period_code = options["period"]
        if period_code > MAX_PERIOD_CODE or period_code < 0:
            self.stdout.write(
                self.style.ERROR(f"Valid Period is between 0 and {MAX_PERIOD_CODE}.")
            )
            return

        if period_code:
            restore_archive(period_code)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Data restored to archive for period {period_code}."
                )
            )
        else:
            restore_last_end_of_month_archive()
            self.stdout.write(
                self.style.SUCCESS("Data restored to latest for period {period_code}.")
            )
