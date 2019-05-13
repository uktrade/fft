from core.models import FinancialYear

import factory


class FinancialYearFactory(factory.DjangoModelFactory):
    """
        Define FinancialYear Factory
    """

    class Meta:
        model = FinancialYear
