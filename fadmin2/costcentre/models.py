from django.db import models
from core.metamodels import TimeStampedModel, LogChangeModel

class DepartmentalGroup(TimeStampedModel, LogChangeModel):
    group_code = models.CharField('Group', primary_key=True, max_length=6)
    group_name = models.CharField('Description', max_length=300)

    def __str__(self):
        return str(self.group_code) + ' - ' + str(self.group_name)


class Directorate(TimeStampedModel, LogChangeModel):
    directorate_code = models.CharField('Directorate', primary_key=True, max_length=6)
    directorate_name = models.CharField('Description', max_length=300)
    group = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.directorate_code) + ' - ' + str(self.directorate_name)


class CostCentre(TimeStampedModel, LogChangeModel):
    cost_centre_code = models.CharField('Cost centre', primary_key=True, max_length=6)
    cost_centre_name = models.CharField('Description', max_length=300)
    # oracle_cost_centre_name = models.CharField('Oracle Description', max_length=300, null=True)
    directorate = models.ForeignKey(Directorate, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.cost_centre_code) + ' - ' + str(self.cost_centre_name)


class Programme(TimeStampedModel, LogChangeModel):
    programme_code = models.CharField('Programme Code', primary_key=True, max_length=50)
    programme_description = models.CharField('Description', max_length=100)
    budget_type = models.CharField('Budget Type', max_length=100)

    def __str__(self):
       return self.programme_code + ' - ' + self.programme_description

