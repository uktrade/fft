from django.db import models
from core.metamodels import TimeStampedModel
from costcentre.models  import  DepartmentalGroup, CostCentre, Programme
from chartofaccountDIT.models import NaturalCode
# salaries data

# define a choice field for this
class Grade(models.Model):
    grade = models.CharField(primary_key=True, max_length=50)
    order = models.IntegerField
    def __str__(self):
       return self.grade


# Pre-calculated salary averages, used for the forecast
class SalaryMonthlyAverage(models.Model):
    AVERAGETYPE_CHOICES = (('CC', 'CostCentre'),
                           ('DIR','Directorate'),
                           ('DG','DepartmentalGroup'),)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    average_type = models.CharField(max_length=50, choices=AVERAGETYPE_CHOICES)
    average_by = models.CharField(max_length=50)
    average_value = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return self.average_type


# Vacancies
class VacanciesHeadCount(models.Model):
    slot_code = models.CharField(max_length=100, primary_key=True)
    vacancy_grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    year = models.IntegerField()
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
    apr = models.BooleanField()
    may = models.BooleanField()
    jun = models.BooleanField()
    jul = models.BooleanField()
    aug = models.BooleanField()
    sep = models.BooleanField()
    oct = models.BooleanField()
    nov = models.BooleanField()
    dec = models.BooleanField()
    jan = models.BooleanField()
    feb = models.BooleanField()
    mar = models.BooleanField()
    HR_reason = models.CharField(max_length=50)  # only two values are valid

    def __str__(self):
       return self.slot_code



class PayModel(models.Model):
    group_code = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    year = models.IntegerField()
    apr = models.DecimalField(max_digits=18, decimal_places=1)
    may = models.DecimalField(max_digits=18, decimal_places=1)
    jun = models.DecimalField(max_digits=18, decimal_places=1)
    jul = models.DecimalField(max_digits=18, decimal_places=1)
    aug = models.DecimalField(max_digits=18, decimal_places=1)
    sep = models.DecimalField(max_digits=18, decimal_places=1)
    oct = models.DecimalField(max_digits=18, decimal_places=1)
    nov = models.DecimalField(max_digits=18, decimal_places=1)
    dec = models.DecimalField(max_digits=18, decimal_places=1)
    jan = models.DecimalField(max_digits=18, decimal_places=1)
    feb = models.DecimalField(max_digits=18, decimal_places=1)
    mar = models.DecimalField(max_digits=18, decimal_places=1)


class PayCostHeadCount(models.Model):
    staff_number = models.IntegerField()
    year = models.IntegerField()
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
    natural_account_code = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
    apr = models.BooleanField()
    may = models.BooleanField()
    jun = models.BooleanField()
    jul = models.BooleanField()
    aug = models.BooleanField()
    sep = models.BooleanField()
    oct = models.BooleanField()
    nov = models.BooleanField()
    dec = models.BooleanField()
    jan = models.BooleanField()
    feb = models.BooleanField()
    mar = models.BooleanField()


class AdminPayModel(models.Model):
    group_code = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)
    year = models.IntegerField()
    pay_rise = models.DecimalField(max_digits=18, decimal_places=2)
    Vacancy = models.DecimalField(max_digits=18, decimal_places=2)
    GAE = models.DecimalField(max_digits=18, decimal_places=2)
    SCS_percent = models.DecimalField(max_digits=18, decimal_places=2)
    SCS_number = models.DecimalField(max_digits=18, decimal_places=2)
    indicative_budget = models.IntegerField()


