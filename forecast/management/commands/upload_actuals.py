from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from forecast.import_actuals import upload_trial_balance_report


class Command(BaseCommand):
    help = "Upload the Trial Balance for a specific month"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("month", type=int)
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        month = options["month"]
        year = options["financial_year"]

        upload_trial_balance_report(path, month, year)
        self.stdout.write(
            self.style.SUCCESS(
                "Actual for period {} added".format(
                    month
                )
            )
        )
