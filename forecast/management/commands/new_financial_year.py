from django.core.management import call_command
from django.core.management.base import CommandError

from chartofaccountDIT.models import ExpenditureCategory
from core.utils.command_helpers import CommandWithUserCheck, get_no_answer
from core.utils.generic_helpers import (
    create_financial_year_display,
    get_current_financial_year,
    get_year_display,
)
from forecast.models import FinancialCode
from forecast.utils.import_helpers import VALID_ECONOMIC_CODE_LIST


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
        try:
            pre_new_financial_year_checks()
        except NewFinancialYearError as err:
            raise CommandError(str(err)) from err

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


class NewFinancialYearError(Exception):
    pass


def pre_new_financial_year_checks() -> None:
    """Pre-flight checks for changing to a new financial year.

    This function will raise `NewFinancialYearError` if any issues are found.

    Checks:
        - Look for used NACs with invalid economic budget codes.
        - Look for budget categories without a budget code.
        - Look for budget categories without a budget grouping.
    """
    # It's possible this needs to be scoped to a financial year in the future.
    problem_nacs = FinancialCode.objects.exclude(
        natural_account_code__economic_budget_code__in=VALID_ECONOMIC_CODE_LIST
    )

    if bool(problem_nacs):
        problem_nac_ids = [str(nac.natural_account_code) for nac in problem_nacs]
        raise NewFinancialYearError(
            f"NACs with invalid economic budget codes: {", ".join(problem_nac_ids)}"
        )

    problem_expenditure_categories = ExpenditureCategory.objects.filter(
        linked_budget_code__isnull=True
    )

    if bool(problem_expenditure_categories):
        problem_ids = [str(x.pk) for x in problem_expenditure_categories]
        raise NewFinancialYearError(
            f"Budget categories without a budget code assigned: {', '.join(problem_ids)}"
        )

    problem_expenditure_categories = ExpenditureCategory.objects.filter(
        NAC_category__isnull=True
    )

    if bool(problem_expenditure_categories):
        problem_ids = [str(x.pk) for x in problem_expenditure_categories]
        raise NewFinancialYearError(
            f"Budget categories without a budget grouping assigned: {', '.join(problem_ids)}"
        )
