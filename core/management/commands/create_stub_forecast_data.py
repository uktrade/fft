from django.core.management.base import BaseCommand

from chartofaccountDIT.models import NaturalCode, ProgrammeCode

from core.models import FinancialYear

from costcentre.models import CostCentre

from forecast.models import FinancialPeriod, MonthlyFigure


def monthly_figures_clear():
    MonthlyFigure.objects.all().delete()


def monthly_figures_create():
    monthly_figures_clear()
    current_financial_year = FinancialYear.objects.get(current=True)
    cost_centre_fk = CostCentre.objects.first()
    programme_list = ProgrammeCode.objects.all()
    natural_account_list = NaturalCode.objects.all()
    financial_periods = FinancialPeriod.objects.exclude(
        period_long_name__icontains="adj"
    )
    monthly_amount = 0
    for programme_fk in programme_list:
        monthly_amount += 10
        for natural_account_code_fk in natural_account_list:
            for f in financial_periods:
                MonthlyFigure.objects.create(
                    financial_year=current_financial_year,
                    financial_period=f,
                    programme=programme_fk,
                    cost_centre=cost_centre_fk,
                    amount=monthly_amount,
                    natural_account_code=natural_account_code_fk,
                )
                monthly_amount += 1

        for i in range(1, 3):
            actual = FinancialPeriod.objects.get(financial_period_code=i)
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
