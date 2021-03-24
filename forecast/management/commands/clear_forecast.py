from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django.db import connection

from core.utils.command_helpers import get_no_answer
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_year_display,
)

from end_of_month.models import EndOfMonthStatus

from previous_years.models import ArchivedFinancialCode


class Command(BaseCommand):
    help = "Delete all forecast/actual/budget figures from the current year"

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Tells Django to NOT prompt the user for input of any kind.",
        )

    def handle(self, *args, **options):
        self.interactive = options["interactive"]
        current_year = get_current_financial_year()
        current_year_display = get_year_display(current_year)
        error_message = (
            f"forecast/actual/budget figures "
            f"for {current_year_display} not deleted."
        )

        if not ArchivedFinancialCode.objects.filter(
            financial_year=current_year
        ).count():
            # If the archive does not exists, ask the users if they want to proceed.
            # If we are not asking questions, consider it a fatal error and exit.
            if self.interactive:
                prompt = (
                    f"The figures for the financial year {current_year_display} "
                    f"are not archived.\n"
                )
                self.stdout.write(self.style.WARNING(prompt))
                abort = get_no_answer()
            else:
                abort = True
                error_message = (
                    f"ABORT (--noinput) - forecast/actual/budget figures "
                    f"for {current_year_display} not deleted."
                )

            if abort:
                self.stdout.write(self.style.ERROR(error_message))
                raise CommandError(error_message)
                return

        if self.interactive:
            prompt = (
                f"All the forecast/actual/budget figures "
                f"for {current_year_display} will be deleted.\n"
                f"This operation cannot be undone.\n"
            )

            self.stdout.write(self.style.WARNING(prompt))
            if get_no_answer():
                self.stdout.write(self.style.ERROR(error_message))
                raise CommandError(error_message)
                return

        EndOfMonthStatus.objects.all().update(
            archived=False, archived_by=None, archived_date=None,
        )

        # Use sql to delete the figure for performance reason.
        # The sql is 1000 times faster than queryset.delete()
        # The displayed forecast is in a strange state during the deletion, so
        # the performance is important. Otherwise we will need to switch FFT during
        # the deletion.
        with connection.cursor() as cursor:
            sql_delete = (
                f"DELETE FROM forecast_budgetmonthlyfigure "
                f"WHERE financial_year_id = {current_year} "
                f"OR financial_year_id IS NULL;"
            )
            cursor.execute(sql_delete)
            sql_delete = (
                f"DELETE FROM end_of_month_monthlytotalbudget "
                f"WHERE financial_year_id = {current_year} "
                f"OR financial_year_id IS NULL;"
            )
            cursor.execute(sql_delete)

            sql_delete = (
                f"DELETE FROM forecast_forecastmonthlyfigure "
                f"WHERE financial_year_id = {current_year} "
                f"OR financial_year_id IS NULL;"
            )
            cursor.execute(sql_delete)

            sql_delete = "DELETE FROM forecast_financialcode;"
            cursor.execute(sql_delete)

        self.stdout.write(
            self.style.SUCCESS(
                f"forecast/actual/budget figures for {current_year_display} "
                f"deleted."
            )
        )
