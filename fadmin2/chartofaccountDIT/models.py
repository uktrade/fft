from django.db import models
from core.metamodels import TimeStampedModel
from treasuryCOA.models import L5Account


# Other members of Account Codes
class Analysis1(TimeStampedModel):
    analysis1_code = models.CharField(primary_key=True, max_length=50)
    analysis1_description = models.CharField(max_length=300)

    def __str__(self):
       return self.analysis1_code + ' - ' + self.analysis1_description

    class Meta:
        verbose_name_plural = "Analysis Codes 1"


class Analysis2(TimeStampedModel):
    analysis2_code = models.CharField(primary_key=True, max_length=50)
    analysis2_description = models.CharField(max_length=300)

    def __str__(self):
       return self.analysis2_code + ' - ' + self.analysis2_description

    class Meta:
        verbose_name_plural = "Analysis Codes 2"


# Category defined by DIT
class NACCategory(TimeStampedModel):
    NAC_category_description = models.CharField(max_length=255, verbose_name='Nac Category')

    def __str__(self):
        return str(self.NAC_category_description)


class ExpenditureCategory(TimeStampedModel):
    grouping_description = models.CharField(max_length=255, verbose_name='Expenditure Category')
    linked_budget_code = models.ForeignKey('NaturalCode', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Budget Code')
    NAC_category = models.ForeignKey(NACCategory,on_delete=models.PROTECT, blank=True, null=True, verbose_name='Budget Grouping')
    description = models.CharField(max_length=5000, blank=True, null=True)
    further_description = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return str(self.NAC_category) + ' - ' + str(self.grouping_description)


# define level1 values: Capital, staff, etc is Level 1 in UKTI nac hierarchy
class NaturalCode(models.Model):
    natural_account_code = models.IntegerField(primary_key=True, verbose_name = 'NAC')
    natural_account_code_description = models.CharField(max_length=200, verbose_name='NAC Description')
    account_L5_code = models.ForeignKey(L5Account,on_delete=models.PROTECT, blank=True, null=True)
    expenditure_category = models.ForeignKey( ExpenditureCategory, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Budget Category')
    used_for_budget = models.BooleanField(default=False)
    used_by_DIT = models.BooleanField(default=False)

    def __str__(self):
        return str(self.natural_account_code) + ' - ' + self.natural_account_code_description

