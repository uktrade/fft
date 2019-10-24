from core.metamodels import LogChangeModel, TimeStampedModel

from costcentre.models import CostCentre, DepartmentalGroup

from django.db import models


# salaries data
# define a choice field for this
class Grade(models.Model):
    grade = models.CharField(primary_key=True, max_length=10)
    gradedescription = models.CharField("Grade Description", max_length=50)
    order = models.IntegerField

    def __str__(self):
        return self.grade

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"


class DITPeople(TimeStampedModel, LogChangeModel):
    employee_number = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True, blank=True)
    cost_centre = models.ForeignKey(
        CostCentre, on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return self.surname + " " + self.name

    class Meta:
        verbose_name = "DIT People"
        verbose_name_plural = "DIT People"
        ordering = ["surname"]


# Pre-calculated salary averages, used for the forecast
class SalaryMonthlyAverage(models.Model):
    AVERAGETYPE_CHOICES = (
        ("CC", "CostCentre"),
        ("DIR", "Directorate"),
        ("DG", "DepartmentalGroup"),
    )
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    average_type = models.CharField(max_length=50, choices=AVERAGETYPE_CHOICES)
    average_by = models.CharField(max_length=50)
    average_value = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return self.average_type


# Vacancies
# class VacanciesHeadCount(TimeStampedModel):
#     slot_code = models.CharField(max_length=100, primary_key=True)
#     vacancy_grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
#     year = models.IntegerField()
#     cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
#     programme = models.ForeignKey(ProgrammeCode, on_delete=models.PROTECT)
#     apr = models.BooleanField()
#     may = models.BooleanField()
#     jun = models.BooleanField()
#     jul = models.BooleanField()
#     aug = models.BooleanField()
#     sep = models.BooleanField()
#     oct = models.BooleanField()
#     nov = models.BooleanField()
#     dec = models.BooleanField()
#     jan = models.BooleanField()
#     feb = models.BooleanField()
#     mar = models.BooleanField()
#     HR_reason = models.CharField(max_length=50)  # only two values are valid
#
#     def __str__(self):
#        return self.slot_code


class PayModel(TimeStampedModel):
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


# class PayCostHeadCount(TimeStampedModel):
#     staff_number = models.IntegerField()
#     year = models.IntegerField()
#     cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
#     programme = models.ForeignKey(ProgrammeCode, on_delete=models.PROTECT)
#     natural_account_code = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
#     apr = models.BooleanField()
#     may = models.BooleanField()
#     jun = models.BooleanField()
#     jul = models.BooleanField()
#     aug = models.BooleanField()
#     sep = models.BooleanField()
#     oct = models.BooleanField()
#     nov = models.BooleanField()
#     dec = models.BooleanField()
#     jan = models.BooleanField()
#     feb = models.BooleanField()
#     mar = models.BooleanField()
#


class AdminPayModel(TimeStampedModel):
    group_code = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)
    year = models.IntegerField()
    pay_rise = models.DecimalField(max_digits=18, decimal_places=2)
    Vacancy = models.DecimalField(max_digits=18, decimal_places=2)
    GAE = models.DecimalField(max_digits=18, decimal_places=2)
    SCS_percent = models.DecimalField(max_digits=18, decimal_places=2)
    SCS_number = models.DecimalField(max_digits=18, decimal_places=2)
    indicative_budget = models.IntegerField()
