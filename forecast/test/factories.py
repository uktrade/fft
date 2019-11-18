import factory

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear

from costcentre.test.factories import CostCentreFactory

from forecast.models import (
    Budget,
    FinancialPeriod,
    ForecastPermission,
    MonthlyFigure,
)


class FinancialPeriodFactory(factory.DjangoModelFactory):

    class Meta:
        model = FinancialPeriod

    financial_period_code = 1
    period_long_name = "April"
    period_short_name = "apr"
    period_calendar_code = 4


class BudgetFactory(factory.DjangoModelFactory):
    """
    Define Budget Factory
    """

    class Meta:
        model = Budget


class MonthlyFigureFactory(factory.DjangoModelFactory):
    """
    Define MonthlyFigure Factory
    """
    programme = factory.SubFactory(ProgrammeCodeFactory)
    cost_centre = factory.SubFactory(CostCentreFactory)
    natural_account_code = factory.SubFactory(NaturalCodeFactory)
    financial_year = factory.Iterator(FinancialYear.objects.all())
    financial_period = factory.Iterator(FinancialPeriod.objects.all())
    amount = 123456

    class Meta:
        model = MonthlyFigure


class ForecastPermissionFactory(factory.DjangoModelFactory):

    class Meta:
        model = ForecastPermission
