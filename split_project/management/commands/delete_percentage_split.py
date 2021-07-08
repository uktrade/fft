from django.db.models import F

from core.utils.command_helpers import CommandUpload
from core.utils.generic_helpers import get_current_financial_year

from forecast.models import (
    MAX_PERIOD_CODE,
    FinancialPeriod,
    ForecastMonthlyFigure,
)

from split_project.models import PaySplitCoefficient


class Command(CommandUpload):
    help = "Remove the project split"

    def add_arguments(self, parser):
        parser.add_argument("financial_period")

    def handle(self, *args, **options):
        financial_period = int(options["financial_period"])

        if financial_period > MAX_PERIOD_CODE or financial_period < 0:
            self.stdout.write(
                self.style.ERROR("Valid Period is between 1 and {MAX_PERIOD_CODE}.")
            )
            return

        financial_period_obj = FinancialPeriod.objects.get(
            financial_period_code=financial_period
        )

        if not financial_period_obj.actual_loaded:
            self.stdout.write(
                self.style.ERROR(
                    f"This command can only be applied to actuals and "
                    f"there are no actuals for the selected period "
                    f"{financial_period_obj.period_long_name}."
                )
            )
            return

        current_year = get_current_financial_year()

        ForecastMonthlyFigure.objects.filter(
            financial_year_id=current_year,
            financial_period=financial_period_obj,
            archived_status__isnull=True,
        ).update(amount=F("oracle_amount"))

        PaySplitCoefficient.objects.filter(
            financial_period=financial_period_obj,
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted project split "
                f"for {financial_period_obj.period_long_name}."
            )
        )
