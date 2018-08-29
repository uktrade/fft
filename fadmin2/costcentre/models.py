from django.db import models
from core.metamodels import TimeStampedModel, LogChangeModel


class DepartmentalGroup(TimeStampedModel, LogChangeModel):
    group_code = models.CharField('Group', primary_key=True, max_length=6)
    group_name = models.CharField('Group Name', max_length=300)
    director_general = models.ForeignKey('payroll.DITPeople', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.group_name)


class Directorate(TimeStampedModel, LogChangeModel):
    directorate_code = models.CharField('Directorate', primary_key=True, max_length=6)
    directorate_name = models.CharField('Directorate Name', max_length=300)
    director = models.ForeignKey('payroll.DITPeople', on_delete=models.PROTECT, null=True, blank=True)
    group = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.directorate_name)


class CostCentre(TimeStampedModel, LogChangeModel):
    cost_centre_code = models.CharField('Cost Centre Code', primary_key=True, max_length=6)
    cost_centre_name = models.CharField('Cost Centre Name', max_length=300)
    directorate = models.ForeignKey(Directorate, on_delete=models.PROTECT)
    deputy_director = models.ForeignKey('payroll.DITPeople', on_delete=models.PROTECT, related_name='deputy_director', null=True, blank=True)
    business_partner = models.ForeignKey('payroll.DITPeople', verbose_name='Finance Business Partner', on_delete=models.PROTECT, related_name='business_partner', null=True, blank=True)

    def __str__(self):
        return str(self.cost_centre_code) + ' - ' + str(self.cost_centre_name)


class Programme(TimeStampedModel, LogChangeModel):
    programme_code = models.CharField('Programme Code', primary_key=True, max_length=50)
    programme_description = models.CharField('Programme Name', max_length=100)
    budget_type = models.CharField('Budget Type', max_length=100)

    def __str__(self):
       return self.programme_code + ' - ' + self.programme_description

