from treasuryCOA.models import HistoricL5Account, L1Account, L2Account, L3Account, L4Account, L5Account

import factory


class L1AccountFactory(factory.DjangoModelFactory):
    """
    Define L1Account Factory
    """

    class Meta:
        model = L1Account


class L2AccountFactory(factory.DjangoModelFactory):
    """
    Define L2Account Factory
    """

    class Meta:
        model = L2Account


class L3AccountFactory(factory.DjangoModelFactory):
    """
    Define L3Account Factory
    """

    class Meta:
        model = L3Account


class L4AccountFactory(factory.DjangoModelFactory):
    """
    Define L4Account Factory
    """

    class Meta:
        model = L4Account


class L5AccountFactory(factory.DjangoModelFactory):
    """
    Define L5Account Factory
    """

    class Meta:
        model = L5Account


class HistoricL5AccountFactory(factory.DjangoModelFactory):
    """
    Define HistoricL5Account Factory
    """

    class Meta:
        model = HistoricL5Account
