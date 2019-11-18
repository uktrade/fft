import factory

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear

from costcentre.test.factories import CostCentreFactory

from forecast.models import (
    FinancialPeriod,
    ForecastActualBudgetFigure,
    ForecastPermission,
)


class ForecastActualBudgetFigureFactory(factory.DjangoModelFactory):
    """
    Define ForecastActualBudgetFigure Factory
    """
    programme = factory.SubFactory(ProgrammeCodeFactory)
    cost_centre = factory.SubFactory(CostCentreFactory)
    natural_account_code = factory.SubFactory(NaturalCodeFactory)
    financial_year = factory.Iterator(FinancialYear.objects.all())
    financial_period = factory.Iterator(FinancialPeriod.objects.all())
    amount = 123456

    class Meta:
        model = ForecastActualBudgetFigure


class ForecastPermissionFactory(factory.DjangoModelFactory):

    class Meta:
        model = ForecastPermission
