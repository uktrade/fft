import datetime

from django.core.management.base import BaseCommand, CommandError

from core.models import FinancialYear
from core.utils.generic_helpers import get_financial_year_obj


class Command(BaseCommand):
    help = (
        "Set the current financial year to the year passed as argument.\n"
        "If no argument is given, set the current financial year "
        "to the current calendar year"
    )

    def add_arguments(self, parser):
        parser.add_argument("year", type=int, nargs="?", default=0)

    def handle(self, *args, **options):
        new_financial_year = options.get("year")
        if not new_financial_year:
            today = datetime.datetime.now()
            new_financial_year = today.year
        if new_financial_year < 2000:
            raise CommandError(
                f"argument year '{new_financial_year}' invalid. " f"Use xxxx format."
            )

        # Clear the current flag
        year_obj = FinancialYear.objects.filter(current=True)
        if year_obj.count():
            previous_financial_year = year_obj.first().financial_year_display
            year_obj.update(current=False)
        else:
            previous_financial_year = "Current year undefined"
        new_year_obj = get_financial_year_obj(new_financial_year)
        new_year_obj.current = True
        new_year_obj.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Current financial year changed from "
                f"'{previous_financial_year}'"
                f" to '{new_year_obj.financial_year_display}'."
            )
        )
