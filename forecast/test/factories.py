import factory

from chartofaccountDIT.test.factories import NaturalCodeFactory, ProgrammeCodeFactory
from core.models import FinancialYear
from costcentre.test.factories import CostCentreFactory
from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastEditState,
    ForecastMonthlyFigure,
    FutureForecastEditState,
    UnlockedForecastEditor,
)


class FinancialPeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FinancialPeriod

    financial_period_code = 1
    period_long_name = "April"
    period_short_name = "apr"
    period_calendar_code = 4


class FinancialCodeFactory(factory.django.DjangoModelFactory):
    programme = factory.SubFactory(ProgrammeCodeFactory)
    cost_centre = factory.SubFactory(CostCentreFactory)
    natural_account_code = factory.SubFactory(NaturalCodeFactory)

    class Meta:
        model = FinancialCode


class BudgetMonthlyFigureFactory(factory.django.DjangoModelFactory):
    financial_code = factory.SubFactory(FinancialCodeFactory)
    financial_year = factory.Iterator(FinancialYear.objects.all())
    financial_period = factory.Iterator(FinancialPeriod.objects.all())


class BudgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BudgetMonthlyFigure


class FinancialCodeFactory(factory.django.DjangoModelFactory):
    programme = factory.SubFactory(ProgrammeCodeFactory)
    cost_centre = factory.SubFactory(CostCentreFactory)
    natural_account_code = factory.SubFactory(NaturalCodeFactory)

    class Meta:
        model = FinancialCode


class MonthlyFigureFactory(factory.django.DjangoModelFactory):
    financial_year = factory.Iterator(FinancialYear.objects.all())
    financial_period = factory.Iterator(FinancialPeriod.objects.all())
    financial_code = factory.SubFactory(FinancialCodeFactory)
    amount = 123456

    class Meta:
        model = ForecastMonthlyFigure


class ForecastEditStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ForecastEditState


class FutureForecastEditStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FutureForecastEditState


class UnlockedForecastEditorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UnlockedForecastEditor
