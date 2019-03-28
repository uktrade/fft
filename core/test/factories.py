import factory

from core.models import FinancialYear


class FinancialYearFactory(factory.DjangoModelFactory):
    """
        Define FinancialYear Factory
    """

    class Meta:
        model = FinancialYear



