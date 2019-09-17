from django.core.management.base import BaseCommand
import core

from core.models import FinancialYear

from costcentre.models import (
    CostCentre,
    DepartmentalGroup,
    Directorate,
)
from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    BudgetType,
    ExpenditureCategory,
    NACCategory,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)


def monthly_figures_clear():
    MonthlyFigure.objects.all().delete()


def monthly_figures_create():
    monthly_figures_clear()
    current_financial_year = FinancialYear.objects.get(current=True)
    cost_centre_fk = CostCentre.objects.first()
    programme_code_ame_fk = ProgrammeCode.objects.filter(budget_type_fk__budget_type_key='AME').first()
    programme_del_fk = ProgrammeCode.objects.filter(budget_type_fk__budget_type_key='DEL').first()
    programme_admin_fk = ProgrammeCode.objects.filter(budget_type_fk__budget_type_key='ADMIN').first()
    programme_list = [programme_code_ame_fk, programme_del_fk, programme_admin_fk]
    natural_account_code_fk = NaturalCode.objects.first()
    financial_periods = FinancialPeriod.objects.exclude(period_long_name__icontains='adj')
    base_amount = 10
    for programme_fk in programme_list:
        base_amount *= 10
        monthly_amount = base_amount
        for f in financial_periods:
            MonthlyFigure.objects.create(
                financial_year=current_financial_year,
                financial_period=f,
                programme=programme_fk,
                cost_centre=cost_centre_fk,
                amount=monthly_amount,
                natural_account_code=natural_account_code_fk
            )
            monthly_amount += 1


class Command(BaseCommand):
    help = 'Create stub forecast data. Use --delete to clear the data'
    arg_name = 'what'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete stub data instead of creating it',
        )

    def handle(self, *args, **options):
        if options['delete']:
            monthly_figures_clear()
            msg = 'cleared'
        else:
            monthly_figures_create()
            msg = 'created'
        self.stdout.write(self.style.SUCCESS('Successfully {} stub forecast data.'.format(msg)))
