from forecast.models import ADIReport, Budget, FinancialCode, \
    FinancialPeriod, MonthlyFigure, OSCARReturn

import factory


class FinancialPeriodFactory(factory.DjangoModelFactory):
    """
    Define FinancialPeriod Factory
    """

    class Meta:
        model = FinancialPeriod


class FinancialCodeFactory(factory.DjangoModelFactory):
    """
    Define FinancialCode Factory
    """

    class Meta:
        model = FinancialCode


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

    class Meta:
        model = MonthlyFigure


class OSCARReturnFactory(factory.DjangoModelFactory):
    """
    Define OSCARReturn Factory
    """

    class Meta:
        model = OSCARReturn


class ADIReportFactory(factory.DjangoModelFactory):
    """
    Define ADIReport Factory
    """

    class Meta:
        model = ADIReport


class FinancialCodeFactory(factory.DjangoModelFactory):
    """
    Define FinancialCode Factory
    """

    class Meta:
        model = FinancialCode


