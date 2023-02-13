from django.core.management.base import BaseCommand

from core.utils.generic_helpers import get_current_financial_year
from end_of_month.monthly_outturn import (
    OutturnInvalidPeriodError,
    OuturnNotArchivedMonthError,
    create_outturn_for_variance,
    validate_period_for_outturn,
)


class Command(BaseCommand):
    help = "Calculate previous period outturns. Valid periods between 1 and 14"

    def add_arguments(self, parser):
        parser.add_argument("period", type=int)

        # Named (optional) arguments
        parser.add_argument(
            "--latest",
            action="store_true",
            help="Create the previous outturn used by the current period",
        )

    def handle(self, *args, **options):
        try:
            period_code = options["period"]
            try:
                validate_period_for_outturn(period_code)
            except OutturnInvalidPeriodError:
                self.stdout.write(self.style.ERROR("Valid Period is between 1 and 15."))
                return
            except OuturnNotArchivedMonthError:
                self.stdout.write(
                    self.style.ERROR("The selected period has not yet been archived.")
                )
                return
            if options["latest"]:
                use_for_current = True
            else:
                use_for_current = False
            create_outturn_for_variance(
                period_code, get_current_financial_year(), use_for_current
            )
            self.stdout.write(
                self.style.SUCCESS(f"Outturn for period {period_code} calculated.")
            )
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"An error occured: {ex}"))
