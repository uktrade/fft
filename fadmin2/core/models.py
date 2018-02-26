from django.db import models


# Remember all fields should be null = true

# Cost Centre hierarchy
class DepartmentalGroup(models.Model):
    GroupCode = models.CharField(primary_key=True, max_length=10)
    GroupName = models.CharField(max_length=300)

    def __str__(self):
        return self.GroupCode


class Directorate(models.Model):
    DirectorateCode = models.CharField(primary_key=True, max_length=10)
    DirectorateName = models.CharField(max_length=300)
    GroupCode = models.ForeignKey(DepartmentalGroup)

    def __str__(self):
        return self.DirectorateCode


class CostCentre(models.Model):
    CCCode = models.CharField(primary_key=True, max_length=10)
    CCName = models.CharField(max_length=300)
    Directorate = models.ForeignKey(Directorate)

    def __str__(self):
        return self.CCCode


#Other members of Account Codes
class Analysis1(models.Model):
   Analysis1Code = models.CharField(primary_key=True, max_length=50)
   Analysis1Description = models.CharField(max_length=300)

   def __str__(self):
       return self.Analysis1Code


class Analysis2(models.Model):
   Analysis2Code = models.CharField(primary_key=True, max_length=50)
   Analysis2Description = models.CharField(max_length=300)

   def __str__(self):
       return self.Analysis2Code


class NaturalCode(models.Model):
   NaturalAccountCode = models.IntegerField(primary_key=True)
   NaturalAccountDescription = models.CharField(max_length=200)
   ProgrammeL2 = models.CharField(max_length=200)
   CashNonCash = models.CharField(max_length=100)
   BudgetCategory = models.CharField(max_length=100)
   L5Code = models.CharField(max_length=20)
   L5Name = models.CharField(max_length=200)
   BudgetReportLine = models.CharField(max_length=200)
   L1Code = models.CharField(max_length=20)
   L1Name = models.CharField(max_length=200)
   Level1 = models.CharField(max_length=255)
   Level2 = models.CharField(max_length=255)
   Level3 = models.CharField(max_length=255)

  def __str__(self):
       return self.NaturalAccountCode

class Programme(models.Model):
   ProgrammeCode = models.CharField(primary_key=True, max_length=50)
   ProgrammeDescription = models.CharField(max_length=100)
   Level1 = models.CharField(max_length=100)
   Level2 = models.CharField(max_length=255)
   Level3 = models.CharField(max_length=255)

   def __str__(self):
       return self.ProgrammeCode




class ADIReport(models.Model):
   Year = models.IntegerField()
   Programme = models.ForeignKey(Programme)
   CCCode = models.ForeignKey(CostCentre)
   NaturalAccountCode = models.ForeignKey(NaturalCode)
   Analysis1Code = models.ForeignKey(Analysis1)
   Analysis2Code = models.ForeignKey(Analysis2)
   April = models.DecimalField(max_digits=18, decimal_places=2)
   May = models.DecimalField(max_digits=18, decimal_places=2)
   June = models.DecimalField(max_digits=18, decimal_places=2)
   July = models.DecimalField(max_digits=18, decimal_places=2)
   August = models.DecimalField(max_digits=18, decimal_places=2)
   September = models.DecimalField(max_digits=18, decimal_places=2)
   October = models.DecimalField(max_digits=18, decimal_places=2)
   November = models.DecimalField(max_digits=18, decimal_places=2)
   December = models.DecimalField(max_digits=18, decimal_places=2)
   January = models.DecimalField(max_digits=18, decimal_places=2)
   February = models.DecimalField(max_digits=18, decimal_places=2)
   March = models.DecimalField(max_digits=18, decimal_places=2)
   Adjustment1 = models.DecimalField(max_digits=18, decimal_places=2)
   Adjustment2 = models.DecimalField(max_digits=18, decimal_places=2)
   Adjustment3 = models.DecimalField(max_digits=18, decimal_places=2)
   Narrative = models.CharField(max_length=2000)
   ADI_Type_FK = models.IntegerField()
   DateCreated = models.DateTimeField()
   CreatedBy = models.CharField(max_length=100)
   DateUpdated = models.DateTimeField(blank=True)
   UpdateBy = models.CharField(max_length=100, blank=True)

   def __str__(self):
       return self.CCCode


    
    

# salaries data

#define a chioce filed for this
class Grades(models.Model):
    Grade = models.CharField(primary_key=True, max_length=50)

   def __str__(self):
       return self.Grade


# Precalculated salary averages, used for the forecast
class SalaryMonthlyAverage(models.Model):
    AVERAGETYPE_CHOICES = ('CostCentre',
                    'Directorate',
                    'DepartmentalGroup',)
    Grade = models.ForeignKey(Grades)
    AverageType = models.CharField(max_length=50, choices=AVERAGETYPE_CHOICES)
    AverageBy = models.CharField(max_length=50)
    AverageValue = models.DecimalField(max_digits=18, decimal_places=2)

   def __str__(self):
       return self.AverageType

