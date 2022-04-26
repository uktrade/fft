from django.core.management.base import BaseCommand

from chartofaccountDIT.models import NaturalCode, ProgrammeCode, ProjectCode

from core.models import FinancialYear
from core.utils.generic_helpers import get_financial_year_obj
from costcentre.models import CostCentre

from end_of_month.models import (
    MonthlyTotalBudget,
)

from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)


def clear_figures(financial_year):
    ForecastMonthlyFigure.objects.filter(financial_year=financial_year).delete()
    BudgetMonthlyFigure.objects.filter(financial_year=financial_year).delete()
    MonthlyTotalBudget.objects.filter(financial_year=financial_year).delete()


def create_future_year_figure(future_financial_year):
    clear_figures(future_financial_year)
    cost_centre_fk = CostCentre.objects.first()
    programme_list = ProgrammeCode.objects.all()
    project_list = ProjectCode.objects.all()
    natural_account_list = NaturalCode.objects.all()
    financial_periods = FinancialPeriod.objects.exclude(
        period_long_name__icontains="adj"
    )
    monthly_amount = 1000
    factor = future_financial_year.financial_year - 2000
    budget_amount = 2000 * factor
    monthly_amount_increment = 2000 * factor
    # Several nested loops, to create a reasonable quantity of data.
    for project_code in project_list:
        for programme_fk in programme_list:
            monthly_amount += monthly_amount_increment
            for natural_account_code_fk in natural_account_list:
                financial_code, _ = FinancialCode.objects.get_or_create(
                    programme=programme_fk,
                    cost_centre=cost_centre_fk,
                    natural_account_code=natural_account_code_fk,
                    project_code=project_code,
                )
                financial_code.save()

                for period in financial_periods:
                    ForecastMonthlyFigure.objects.create(
                        financial_year=future_financial_year,
                        financial_period=period,
                        financial_code=financial_code,
                        amount=monthly_amount,
                    )
                    monthly_amount += monthly_amount_increment
                    BudgetMonthlyFigure.objects.create(
                        financial_year=future_financial_year,
                        financial_period=period,
                        financial_code=financial_code,
                        amount=budget_amount,
                    )
                    budget_amount += monthly_amount_increment


class Command(BaseCommand):
    help = (
        "Create stub forecast data for future 3 years. Use --delete to clear the data"
    )
    arg_name = "what"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete stub data instead of creating it",
        )

    def handle(self, *args, **options):
        financial_year = FinancialYear.objects.get(current=True).financial_year

        if options["delete"]:
            action = clear_figures
            msg = "cleared"
        else:
            action = create_future_year_figure
            msg = "created"

        for interval in range(1, 4):
            year_obj = get_financial_year_obj(financial_year + interval)

            action(year_obj)
        self.stdout.write(
            self.style.SUCCESS("Successfully {} stub future forecast data.".format(msg))
        )
