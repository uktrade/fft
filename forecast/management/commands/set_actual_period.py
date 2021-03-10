from django.core.management.base import BaseCommand

from end_of_month.utils import InvalidPeriodError


from forecast.models import (
    MAX_PERIOD_CODE,
    FinancialPeriod,
)


def validate_period_code(period_code):
    if period_code > MAX_PERIOD_CODE or period_code < 1:
        raise InvalidPeriodError()


class Command(BaseCommand):
    help = "Set or clear the Actual uploaded status"

    def add_arguments(self, parser):
        parser.add_argument("period", type=int)
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Set the Actual uploaded status from "
            "the beginning of the financial year until and including the given period."
            "Using --clear clear the Actual uploaded status from the given period "
            "until the end of the financial year. "
            "the argument 'period' is the financial period code "
            "(1 for April, 2 for May, etc.) ",
        )

    def handle(self, *args, **options):
        try:
            period_code = options["period"]
            if period_code > MAX_PERIOD_CODE or period_code < 0:
                self.stdout.write(
                    self.style.ERROR("Valid Period is between 1 and {MAX_PERIOD_CODE}.")
                )
                return
            month_name = FinancialPeriod.objects.get(
                financial_period_code=period_code
            ).period_long_name

            if options["clear"]:
                FinancialPeriod.objects.filter(
                    financial_period_code__gte=period_code
                ).update(actual_loaded=False)
                FinancialPeriod.objects.filter(
                    financial_period_code__lt=period_code
                ).update(actual_loaded=True)
                msg = f"Actual flag cleared up to {month_name}"
            else:
                FinancialPeriod.objects.filter(
                    financial_period_code__lte=period_code
                ).update(actual_loaded=True)
                FinancialPeriod.objects.filter(
                    financial_period_code__gt=period_code
                ).update(actual_loaded=False)

                msg = f"Actual flag set up to {month_name}"
            self.stdout.write(self.style.SUCCESS(msg))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"An error occured: {ex}"))
