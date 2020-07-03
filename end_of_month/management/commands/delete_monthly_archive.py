from django.core.management.base import BaseCommand

from end_of_month.end_of_month_actions import (
    delete_end_of_month_archive,
    delete_last_end_of_month_archive,
)


class Command(BaseCommand):
    help = (
        "Delete archived forecast and budget for a specific period: "
        "1 to 15 starting from April. 0 will delete the latest archive."
    )

    def add_arguments(self, parser):
        parser.add_argument("period", type=int)

    def handle(self, *args, **options):
        period_code = options["period"]
        if period_code > 15 or period_code < 0:
            self.stdout.write(self.style.ERROR("Valid Period is between 1 and 15."))
            return

        if period_code:
            delete_end_of_month_archive(period_code)
            self.stdout.write(
                self.style.SUCCESS(f'Archive for period {period_code} deleted.')
            )
        else:
            delete_last_end_of_month_archive()
            self.stdout.write(
                self.style.SUCCESS(f'Latest archive deleted.')
            )
