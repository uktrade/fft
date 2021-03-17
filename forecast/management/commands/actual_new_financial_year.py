from django.core.management.base import BaseCommand
from django.db.models import F

from forecast.models import FinancialPeriod


class Command(BaseCommand):
    help = "Change the actual load flag for the new financial year."

    def handle(self, *args, **options):
        try:
            FinancialPeriod.objects.all().update(
                actual_loaded_previous_year=F("actual_loaded")
            )
            FinancialPeriod.financial_period_info.reset_actuals()
            self.stdout.write(self.style.SUCCESS("Actual flag cleared."))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"An error occured: {ex}"))
