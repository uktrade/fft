from django.core.management.base import BaseCommand
from django.db.models import F

from chartofaccountDIT.models import (
    NaturalCode,
    ProgrammeCode,
)

from core.models import FinancialYear

from costcentre.models import (
    CostCentre,
    Directorate,
)

from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)

from split_project.models import ProjectSplitCoefficient

# New cost centre code, used only for splitting the actuals
COST_CENTRE_CODE = 87654


def project_split_clear():
    try:
        ProjectSplitCoefficient.objects.all().delete()
        cost_centre_obj = CostCentre.objects.get(pk=COST_CENTRE_CODE)
        financial_codes_queryset = FinancialCode.objects.filter(
            cost_centre=cost_centre_obj
        )
        for financial_code in financial_codes_queryset:
            ForecastMonthlyFigure.objects.filter(financial_code=financial_code).delete()
            financial_code.delete()
        cost_centre_obj.delete()
    except CostCentre.DoesNotExist:
        pass


def monthly_split_create():
    project_split_clear()
    ForecastMonthlyFigure.objects.all().delete()
    BudgetMonthlyFigure.objects.all().delete()
    current_financial_year = FinancialYear.objects.get(current=True)
    cost_centre_obj = CostCentre.objects.create(
        cost_centre_code=COST_CENTRE_CODE,
        active=True,
        cost_centre_name="Cost Centre for split project",
        directorate=Directorate.objects.all().first(),
    )
    programme_obj = ProgrammeCode.objects.all().first()
    natural_account_obj = NaturalCode.objects.all().first()
    financial_periods = FinancialPeriod.objects.exclude(
        period_long_name__icontains="adj"
    )
    # Create the amount to be split
    financial_code_from = FinancialCode.objects.create(
        programme=programme_obj,
        cost_centre=cost_centre_obj,
        natural_account_code=natural_account_obj,
    )
    financial_code_from.save()
    monthly_amount = 1000000

    for period in financial_periods:
        monthly_amount += 10000
        ForecastMonthlyFigure.objects.create(
            financial_year=current_financial_year,
            financial_period=period,
            financial_code=financial_code_from,
            amount=monthly_amount,
            oracle_amount=monthly_amount,
        )

    # Now initialise oracle_amount in every field
    ForecastMonthlyFigure.objects.update(oracle_amount=F("amount"))


class Command(BaseCommand):
    help = "Create stub project split data. Use --delete to clear the data"
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
            project_split_clear()
            msg = "cleared"
        else:
            monthly_split_create()
            msg = "created"
        self.stdout.write(self.style.SUCCESS(f"Successfully {msg} stub forecast data."))
