from django.core.management.base import BaseCommand

from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.models import (
    EndOfMonthStatus,
    MonthlyTotalBudget,
)

from chartofaccountDIT.models import NaturalCode, ProgrammeCode, ProjectCode

from core.models import FinancialYear

from costcentre.models import CostCentre

from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)


def monthly_figures_clear():
    ForecastMonthlyFigure.objects.all().delete()
    BudgetMonthlyFigure.objects.all().delete()
    MonthlyTotalBudget.objects.all().delete()

    financial_period_queryset = FinancialPeriod.objects.all()
    for financial_period in financial_period_queryset:
        financial_period.actual_loaded = False
        financial_period.save()

    month_status_q = EndOfMonthStatus.objects.all()
    for month_status in month_status_q:
        month_status.archived = False
        month_status.save()
    FinancialCode.objects.all().delete()


def monthly_figures_create():
    monthly_figures_clear()
    current_financial_year = FinancialYear.objects.get(current=True)
    cost_centre_fk = CostCentre.objects.first()
    programme_list = ProgrammeCode.objects.all()
    project_list = ProjectCode.objects.all()
    natural_account_list = NaturalCode.objects.all()
    financial_periods = FinancialPeriod.objects.exclude(
        period_long_name__icontains="adj"
    )
    monthly_amount = 0
    budget_amount = 1
    # Several nested loops, to create a reasonable quantity of data.
    for project_code in project_list:
        for programme_fk in programme_list:
            monthly_amount += 10
            for natural_account_code_fk in natural_account_list:
                financial_code = FinancialCode.objects.create(
                    programme=programme_fk,
                    cost_centre=cost_centre_fk,
                    natural_account_code=natural_account_code_fk,
                    project_code=project_code,
                )
                financial_code.save()

                for period in financial_periods:
                    ForecastMonthlyFigure.objects.create(
                        financial_year=current_financial_year,
                        financial_period=period,
                        financial_code=financial_code,
                        amount=monthly_amount,
                    )
                    monthly_amount += 10
                    BudgetMonthlyFigure.objects.create(
                        financial_year=current_financial_year,
                        financial_period=period,
                        financial_code=financial_code,
                        amount=budget_amount,
                    )
                    budget_amount += 1

    for period_id in range(1, 3):
        end_of_month_archive(period_id)
        actual = FinancialPeriod.objects.get(financial_period_code=period_id)
        actual.actual_loaded = True
        actual.save()


class Command(BaseCommand):
    help = "Create stub forecast data. Use --delete to clear the data"
    arg_name = "what"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete stub data instead of creating it",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            monthly_figures_clear()
            msg = "cleared"
        else:
            monthly_figures_create()
            msg = "created"
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully {} stub forecast data.".format(
                    msg
                )
            )
        )
