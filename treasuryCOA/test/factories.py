from treasuryCOA.models import (
    HistoricL5Account,
    L1Account,
    L2Account,
    L3Account,
    L4Account,
    L5Account,
)

import factory


class L1AccountFactory(factory.DjangoModelFactory):
    """
    Define L1Account Factory
    """

    class Meta:
        model = L1Account

    account_l1_code = 1111111


class L2AccountFactory(factory.DjangoModelFactory):
    """
    Define L2Account Factory
    """

    class Meta:
        model = L2Account

    account_l2_code = 1111111
    account_l1 = factory.SubFactory(L1AccountFactory)


class L3AccountFactory(factory.DjangoModelFactory):
    """
    Define L3Account Factory
    """

    class Meta:
        model = L3Account

    account_l3_code = 111111
    account_l2 = factory.SubFactory(L2AccountFactory)


class L4AccountFactory(factory.DjangoModelFactory):
    """
    Define L4Account Factory
    """

    class Meta:
        model = L4Account

    account_l4_code = 111111
    account_l3 = factory.SubFactory(L3AccountFactory)


class L5AccountFactory(factory.DjangoModelFactory):
    """
    Define L5Account Factory
    """

    class Meta:
        model = L5Account

    economic_budget_code = "CAPITAL"
    account_l5_code = 111111
    account_l4 = factory.SubFactory(L4AccountFactory)


class HistoricL5AccountFactory(factory.DjangoModelFactory):
    """
    Define HistoricL5Account Factory
    """

    class Meta:
        model = HistoricL5Account
