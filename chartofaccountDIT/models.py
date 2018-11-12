from core.metamodels import LogChangeModel, TimeStampedModel

from django.db import models

from treasuryCOA.models import L5Account


# Other members of Account Codes
class Analysis1(TimeStampedModel, LogChangeModel):
    analysis1_code = models.CharField('Contract Code', primary_key=True, max_length=50)
    analysis1_description = models.CharField('Contract Name', max_length=300)
    supplier = models.CharField('Supplier', max_length=300, default='')
    pc_reference = models.CharField('PC Reference', max_length=300, default='')

    def __str__(self):
        return self.analysis1_code + ' - ' + self.analysis1_description

    class Meta:
        verbose_name_plural = "Contract Reconciliations (Analysis 1)"
        verbose_name = "Contract Reconciliation (Analysis 1)"


class Analysis2(TimeStampedModel):
    analysis2_code = models.CharField('Market Code', primary_key=True, max_length=50)
    analysis2_description = models.CharField(max_length=300, verbose_name='Market')

    def __str__(self):
        return self.analysis2_code + ' - ' + self.analysis2_description

    class Meta:
        verbose_name = "Market (Analysis 2)"
        verbose_name_plural = "Markets (Analysis 2)"


# Category defined by DIT
class NACCategory(TimeStampedModel, LogChangeModel):
    NAC_category_description = models.CharField(max_length=255, verbose_name='Budget Grouping',
                                                unique=True)

    def __str__(self):
        return str(self.NAC_category_description)

    class Meta:
        verbose_name = "Budget Grouping"
        verbose_name_plural = "Budget Groupings"


class ExpenditureCategory(TimeStampedModel):
    grouping_description = models.CharField(max_length=255, verbose_name='Budget Category',
                                            unique=True)
    linked_budget_code = models.ForeignKey('NaturalCode', on_delete=models.PROTECT,
                                           blank=True, null=True, verbose_name='Budget Code')
    NAC_category = models.ForeignKey(NACCategory, on_delete=models.PROTECT,
                                     blank=True, null=True, verbose_name='Budget Grouping')
    description = models.CharField(max_length=5000, blank=True, null=True)
    further_description = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return str(self.grouping_description)

    class Meta:
        verbose_name = "Budget Category"
        verbose_name_plural = "Budget Categories"


class CommercialCategory(TimeStampedModel, LogChangeModel):
    commercial_category = models.CharField(max_length=255, verbose_name='Commercial Category',
                                           unique=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    approvers = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return str(self.commercial_category)

    class Meta:
        verbose_name = "Commercial Category"
        verbose_name_plural = "Commercial Categories"


# define level1 values: Capital, staff, etc is Level 1 in UKTI nac hierarchy
class NaturalCode(TimeStampedModel, LogChangeModel):
    natural_account_code = models.IntegerField(primary_key=True, verbose_name='NAC')
    natural_account_code_description = models.CharField(max_length=200,
                                                        verbose_name='NAC Description')
    account_L5_code = models.ForeignKey(L5Account, on_delete=models.PROTECT, blank=True, null=True)
    expenditure_category = models.ForeignKey(ExpenditureCategory, verbose_name='Budget Category',
                                             on_delete=models.PROTECT, blank=True, null=True)
    commercial_category = models.ForeignKey(CommercialCategory,
                                            on_delete=models.PROTECT, blank=True, null=True)
    used_for_budget = models.BooleanField(default=False)

    def __str__(self):
        return str(self.natural_account_code) + ' - ' + self.natural_account_code_description

    class Meta:
        verbose_name = "Natural Account Code (NAC)"
        verbose_name_plural = "Natural Account Codes (NAC)"
        ordering = ['natural_account_code']


class ProgrammeCode(TimeStampedModel, LogChangeModel):
    programme_code = models.CharField('Programme Code', primary_key=True, max_length=50)
    programme_description = models.CharField('Programme Name', max_length=100)
    budget_type = models.CharField('Budget Type', max_length=100)

    def __str__(self):
        return self.programme_code + ' - ' + self.programme_description

    class Meta:
        verbose_name = "Programme Code"
        verbose_name_plural = "Programme Codes"


class InterEntityL1(TimeStampedModel, LogChangeModel):
    l1_value = models.CharField('Government Body', primary_key=True, max_length=10)
    l1_description = models.CharField('Government Body Description', max_length=100)

    def __str__(self):
        return self.l1_value + ' - ' + self.l1_description

    class Meta:
        verbose_name = "Government Body"
        verbose_name_plural = "Government Bodies"


class InterEntity(TimeStampedModel, LogChangeModel):
    l2_value = models.CharField('ORACLE - Inter Entity Code', primary_key=True, max_length=10)
    l2_description = models.CharField('ORACLE - Inter Entity Description', max_length=100)
    l1_value = models.ForeignKey(InterEntityL1, on_delete=models.PROTECT)
    cpid = models.CharField('Treasury - CPID (Departmental Code No.)', max_length=10)

    def __str__(self):
        return self.l2_value + ' - ' + self.l2_description

    class Meta:
        verbose_name = "Inter-Entity"
        verbose_name_plural = "Inter-Entities"


class ProjectCode(TimeStampedModel, LogChangeModel):
    project_code = models.CharField('Project Code', primary_key=True, max_length=50)
    project_description = models.CharField(max_length=300, verbose_name='Project Description')

    def __str__(self):
        return self.project_code + ' - ' + self.project_description

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"



