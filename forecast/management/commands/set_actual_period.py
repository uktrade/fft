from django.core.management.base import BaseCommand

from forecast.models import FinancialPeriod


class Command(BaseCommand):
    help = "Set or clear the Actual uploaded status"

    def add_arguments(self, parser):
        parser.add_argument("month", type=int)
        # Named (optional) arguments
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear the Actual uploaded status from "
                 "the given month to the end of the financial year.",
        )

    def handle(self, *args, **options):
        month = options["month"]
        financial_period_code = FinancialPeriod.objects.get(
            period_calendar_code=month
        ).financial_period_code
        if options["clear"]:
            FinancialPeriod.objects.filter(
                financial_period_code__gte=financial_period_code
            ).update(actual_loaded=False)
        else:
            FinancialPeriod.objects.filter(
                financial_period_code__lte=financial_period_code
            ).update(actual_loaded=True)
