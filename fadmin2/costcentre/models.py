from django.db import models
from core.metamodels import TimeStampedModel

class DepartmentalGroup(TimeStampedModel):
    group_code = models.CharField(primary_key=True, max_length=10)
    group_name = models.CharField(max_length=300)
    def __str__(self):
        return self.group_code + ' - ' + self.group_name


class Directorate(TimeStampedModel):
    directorate_code = models.CharField('Directorate', primary_key=True, max_length=10)
    directorate_name = models.CharField(max_length=300)
    group_code = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)

    def __str__(self):
        return self.directorate_code + ' - ' + self.directorate_name


class CostCentre(TimeStampedModel):
    cost_centre_code = models.CharField('cost centre', primary_key=True, max_length=10)
    cost_centre_name = models.CharField('description', max_length=300)
    directorate = models.ForeignKey(Directorate, on_delete=models.PROTECT)

    def __str__(self):
        return self.cost_centre_code + ' - ' + self.cost_centre_name


class Programme(models.Model):
    programme_code = models.CharField('Programme Code', primary_key=True, max_length=50)
    programme_description = models.CharField('Description', max_length=100)
    budget_type = models.CharField('Budget Type', max_length=100)

    def __str__(self):
       return self.programme_code

