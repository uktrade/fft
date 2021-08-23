from django.core.management.base import BaseCommand

from core.utils.generic_helpers import get_current_financial_year

from end_of_month.models import EndOfMonthStatus
from end_of_month.monthly_outturn import create_outturn_for_variance


class Command(BaseCommand):
    help = "Calculate previous period outturns for all the archived periods."

    def handle(self, *args, **options):

        period_list = EndOfMonthStatus.archived_period_objects.archived_list()
        if not period_list:
            self.stdout.write(
                self.style.ERROR("No archived periods in the current year.")
            )
            return

        latest_period = period_list.pop(0)

        current_year = get_current_financial_year()
        create_outturn_for_variance(latest_period[0], current_year, True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Outturn for period {latest_period[1]} calculated."
                f" Used in the current period."
            )
        )

        for period in period_list:
            create_outturn_for_variance(period[0], current_year)
            self.stdout.write(
                self.style.SUCCESS(f"Outturn for period {period[1]} calculated.")
            )
