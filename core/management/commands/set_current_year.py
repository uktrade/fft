import datetime

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from core.models import FinancialYear
from core.utils.generic_helpers import create_financial_year_display


class Command(BaseCommand):
    help = "Set the current financial year."

    def add_arguments(self, parser):
        parser.add_argument("year", type=int, nargs="?", default=0)

    def handle(self, *args, **options):
        calendar_year = options.get("year")
        if not calendar_year:
            today = datetime.datetime.now()
            calendar_year = today.year
        if calendar_year < 2000:
            raise CommandError(
                f"argument year '{calendar_year}' invalid. " f"Use xxxx format."
            )

        # Clear the current flag
        year_obj = FinancialYear.objects.filter(current=True)
        if year_obj.count():
            previous_financial_year = year_obj.first().financial_year_display
            year_obj.update(current=False)
        else:
            previous_financial_year = "Current year undefined"
        year_obj, created = FinancialYear.objects.get_or_create(
            financial_year=calendar_year
        )
        if created:
            year_obj.financial_year_display = create_financial_year_display(
                calendar_year
            )
        new_financial_year = year_obj.financial_year_display
        year_obj.current = True
        year_obj.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Current financial year changed from "
                f"'{previous_financial_year}'"
                f" to '{new_financial_year}'."
            )
        )
