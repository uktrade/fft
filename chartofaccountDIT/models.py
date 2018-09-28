from django.db import models

from core.metamodels import LogChangeModel, TimeStampedModel

from treasuryCOA.models import L5Account


# Other members of Account Codes
class Analysis1(TimeStampedModel):
    analysis1_code = models.CharField(primary_key=True, max_length=50)
    analysis1_description = models.CharField(max_length=300)

    def __str__(self):
        return self.analysis1_code + ' - ' + self.analysis1_description

    class Meta:
        verbose_name_plural = "Contract Reconciliations (Analysis 1)"
        verbose_name = "Contract Reconciliation (Analysis 1)"


class Analysis2(TimeStampedModel):
    analysis2_code = models.CharField(primary_key=True, max_length=50)
    analysis2_description = models.CharField(max_length=300, verbose_name='Market')

    def __str__(self):
        return self.analysis2_code + ' - ' + self.analysis2_description

    class Meta:
        verbose_name = "Market (Analysis 2)"
        verbose_name_plural = "Markets (Analysis 2)"


# Category defined by DIT
class NACCategory(TimeStampedModel):
    NAC_category_description = models.CharField(max_length=255, verbose_name='Budget Grouping',unique=True)

    def __str__(self):
        return str(self.NAC_category_description)

    class Meta:
        verbose_name = "Budget Grouping"
        verbose_name_plural = "Budget Groupings"


class ExpenditureCategory(TimeStampedModel):
    grouping_description = models.CharField(max_length=255, verbose_name='Expenditure Category', unique=True)
    linked_budget_code = models.ForeignKey('NaturalCode', on_delete=models.PROTECT,
                                           blank=True, null=True, verbose_name='Budget Code')
    NAC_category = models.ForeignKey(NACCategory, on_delete=models.PROTECT,
                                     blank=True, null=True, verbose_name='Budget Grouping')
    description = models.CharField(max_length=5000, blank=True, null=True)
    further_description = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return str(self.grouping_description)

    class Meta:
        verbose_name = "Expenditure Category"
        verbose_name_plural = "Expenditure Categories"


class CommercialCategory(TimeStampedModel):
    commercial_category = models.CharField(max_length=255, verbose_name='Commercial Category', unique=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    approvers = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return str(self.commercial_category)

    class Meta:
        verbose_name = "Commercial Category"
        verbose_name_plural = "Commercial Categories"


# define level1 values: Capital, staff, etc is Level 1 in UKTI nac hierarchy
class NaturalCode(TimeStampedModel):
    natural_account_code = models.IntegerField(primary_key=True, verbose_name='NAC')
    natural_account_code_description = models.CharField(max_length=200,
                                                        verbose_name='NAC Description')
    account_L5_code = models.ForeignKey(L5Account, on_delete=models.PROTECT, blank=True, null=True)
    expenditure_category = models.ForeignKey(ExpenditureCategory,
                                             on_delete=models.PROTECT, blank=True, null=True)
    commercial_category = models.ForeignKey(CommercialCategory,
                                            on_delete=models.PROTECT, blank=True, null=True)
    used_for_budget = models.BooleanField(default=False)

    def __str__(self):
        return str(self.natural_account_code) + ' - ' + self.natural_account_code_description

    class Meta:
        verbose_name = "Natural Account Code (NAC)"
        verbose_name_plural = "Natural Account Codes (NAC)"


class ProgrammeCode(TimeStampedModel, LogChangeModel):
    programme_code = models.CharField('Programme Code', primary_key=True, max_length=50)
    programme_description = models.CharField('Programme Name', max_length=100)
    budget_type = models.CharField('Budget Type', max_length=100)

    def __str__(self):
        return self.programme_code + ' - ' + self.programme_description

    class Meta:
        verbose_name = "Programme Code"
        verbose_name_plural = "Programme Codes"
