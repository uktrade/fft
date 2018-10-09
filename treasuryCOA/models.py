from core.metamodels import TimeStampedModel

from django.db import models


# Account codes from Treasury
# the following table could be normalised more, but I don't think it matters
class L1Account(TimeStampedModel):
    account_l1_code = models.BigIntegerField(primary_key=True, verbose_name='account l1 code')
    account_l1_long_name = models.CharField(max_length=255,
                                            verbose_name='account l1 long name', blank=True)
    account_code = models.CharField(max_length=255, verbose_name='accounts code')
    account_l0_code = models.CharField(max_length=255, verbose_name='account l0 code')

    class Meta:
        verbose_name = 'Treasury Level 1 COA'

    def __str__(self):
        return str(self.account_l1_code) + ' - ' + str(self.account_l1_long_name)


class L2Account(TimeStampedModel):
    account_l2_code = models.BigIntegerField(primary_key=True, verbose_name='account l2 code')
    account_l2_long_name = models.CharField(max_length=255,
                                            verbose_name='account l2 long name', blank=True)
    account_l1 = models.ForeignKey(L1Account,
                                   verbose_name='account l1 code', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Treasury Level 2 COA'

    def __str__(self):
        return str(self.account_l2_code) + ' - ' + str(self.account_l2_long_name)


class L3Account(TimeStampedModel):
    account_l3_code = models.BigIntegerField(verbose_name='account l3 code', primary_key=True)
    account_l3_long_name = models.CharField(max_length=255,
                                            verbose_name='account l3 long name', blank=True)
    account_l2 = models.ForeignKey(L2Account,
                                   verbose_name='account l2 code', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Treasury Level 3 COA'

    def __str__(self):
        return str(self.account_l3_code) + ' - ' + str(self.account_l3_long_name)


class L4Account(TimeStampedModel):
    account_l4_code = models.BigIntegerField(verbose_name='account l4 code', primary_key=True)
    account_l4_long_name = models.CharField(max_length=255,
                                            verbose_name='account l4 long name', blank=True)
    account_l3 = models.ForeignKey(L3Account,
                                   verbose_name='account l3 code', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Treasury Level 4 COA'

    def __str__(self):
        return str(self.account_l4_code) + ' - ' + str(self.account_l4_long_name)


class L5Account(TimeStampedModel):
    BOTH = 'BOTH'
    OUTTURN = 'OUTTURN'
    PLANS = 'PLANS'
    USAGECODE_CHOICES = (
        (BOTH, 'BOTH'),
        (OUTTURN, 'OUTTURN'),
        (PLANS, 'PLANS'),
    )
    GROSS = 'GROSS'
    INCOME = 'INCOME'
    UNDEF = 'N/A'
    ESTIMATECODE_CHOICES = (
        (GROSS, 'GROSS'),
        (INCOME, 'INCOME'),
        (UNDEF, 'N/A'),
    )
    account_l5_code = models.BigIntegerField(primary_key=True, verbose_name='account l5 code')
    account_l5_long_name = models.CharField(max_length=255, verbose_name='account l5 long name',
                                            blank=True)
    account_l5_description = models.CharField(max_length=2048, blank=True,
                                              verbose_name='account l5 description')
    account_l4 = models.ForeignKey(L4Account, verbose_name='account l4 code',
                                   on_delete=models.PROTECT)
    economic_budget_code = models.CharField(max_length=255, verbose_name='economic budget code',
                                            blank=True)
    sector_code = models.CharField(max_length=255, verbose_name='sector code', blank=True)
    estimates_column_code = models.CharField(max_length=25, choices=ESTIMATECODE_CHOICES,
                                             default=UNDEF, verbose_name='estimates column code')
    usage_code = models.CharField(max_length=25, choices=USAGECODE_CHOICES, default=BOTH,
                                  verbose_name='usage code', blank=True)
    cash_indicator_code = models.CharField(max_length=5,
                                           verbose_name='cash indicator code', blank=True)

    class Meta:
        verbose_name = 'Treasury Level 5 COA'

    def __str__(self):
        return str(self.account_l5_code) + ' - ' + str(self.account_l5_long_name)
