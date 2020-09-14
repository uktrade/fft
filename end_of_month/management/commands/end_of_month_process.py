from django.core.management.base import BaseCommand

from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.utils import (
    InvalidPeriodError,
    LaterPeriodAlreadyArchivedError,
    PeriodAlreadyArchivedError,
    validate_period_code,
)


class Command(BaseCommand):
    help = (
        "Archive forecast and budget for a specific period: 1 to 12 starting from April"
    )

    def add_arguments(self, parser):
        parser.add_argument("period", type=int)

    def handle(self, *args, **options):
        try:
            period_code = options["period"]
            try:
                validate_period_code(period_code)
            except InvalidPeriodError:
                self.stdout.write(self.style.ERROR("Valid Period is between 1 and 15."))
                return
            except PeriodAlreadyArchivedError:
                self.stdout.write(
                    self.style.ERROR("The selected period has already been archived.")
                )
                return
            except LaterPeriodAlreadyArchivedError:
                self.stdout.write(
                    self.style.ERROR("A later period has already been archived.")
                )
                return
            end_of_month_archive(period_code)
            self.stdout.write(
                self.style.SUCCESS(f'Period {period_code} archived.')
            )
        except Exception as ex:
            self.stdout.write(
                self.style.ERROR(f"An error occured: {ex}")
            )
