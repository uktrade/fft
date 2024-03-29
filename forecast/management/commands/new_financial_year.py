from django.core.management import call_command
from django.core.management.base import CommandError

from core.utils.command_helpers import CommandWithUserCheck, get_no_answer
from core.utils.generic_helpers import (
    create_financial_year_display,
    get_current_financial_year,
    get_year_display,
)


class Command(CommandWithUserCheck):
    help = "Run all the operations required to prepare for the new financial year"
    command_name = __name__

    def run_command(self, message, command_name, *arg, **options):
        self.stdout.write(self.style.WARNING(f"{message}..."))
        try:
            call_command(command_name, *arg, **options)
        except CommandError as ex:
            full_error_message = (
                f"{message} failed. " f"Ex '{ex}'\nMessage: '{self.error_message}'"
            )
            self.stdout.write(self.style.ERROR(full_error_message))
            raise CommandError(full_error_message)

        return True

    def handle_user(self, *args, **options):
        current_financial_year = get_current_financial_year()
        current_financial_year_display = get_year_display(current_financial_year)
        new_financial_year = current_financial_year + 1
        new_financial_year_display = create_financial_year_display(new_financial_year)
        self.error_message = (
            f"Financial year {current_financial_year_display} not changed."
        )

        prompt = (
            f"The financial year will change from  "
            f"{current_financial_year_display} to {new_financial_year_display}.\n"
            f"This operation cannot be undone.\n"
        )

        self.stdout.write(self.style.WARNING(prompt))
        if get_no_answer():
            self.stdout.write(self.style.ERROR(self.error_message))
            raise CommandError(self.error_message)
            return

        if not self.run_command("Archiving chart of account", "archive"):
            return
        if not self.run_command(
            "Archiving current financial year", "archive_current_year"
        ):
            return
        if not self.run_command(
            "Deleting current year figures", "clear_forecast", "--noinput"
        ):
            return
        if not self.run_command(
            f"Setting current financial year to {new_financial_year_display}",
            "set_current_year",
        ):
            return
        if not self.run_command("Clear actual flags", "actual_new_financial_year"):
            return

        self.stdout.write(
            self.style.SUCCESS(f"FFT ready for {new_financial_year_display} ")
        )
