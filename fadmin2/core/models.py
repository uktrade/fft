from django.db import models
from .utils import ChoiceEnum

# Remember all fields should be null = true


# Cost Centre hierarchy
class DepartmentalGroup(models.Model):
    GroupCode = models.CharField(primary_key=True, max_length=10)
    GroupName = models.CharField(max_length=300)

    def __str__(self):
        return self.GroupCode + ' - ' + self.GroupName


class Directorate(models.Model):
    DirectorateCode = models.CharField(primary_key=True, max_length=10)
    DirectorateName = models.CharField(max_length=300)
    GroupCode = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)

    def __str__(self):
        return self.DirectorateCode + ' - ' + self.DirectorateName


class CostCentre(models.Model):
    CCCode = models.CharField('cost centre', primary_key=True, max_length=10)
    CCName = models.CharField('description', max_length=300)
    Directorate = models.ForeignKey(Directorate, on_delete=models.PROTECT)

    def __str__(self):
        return self.CCCode


# Other members of Account Codes
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


# Account codes from Treasury
# the following table could be normalised more, but I don't think it matters
class L1Account(models.Model):
    AccountL1Code = models.BigIntegerField(primary_key=True, verbose_name='account l1 code')
    AccountL1LongName = models.CharField(max_length=255, verbose_name='account l1 long name')
    AccountsCode = models.CharField(max_length=255,  verbose_name='accounts code')
    AccountL0Code = models.CharField(max_length=255, verbose_name='account l0 code')

    class Meta:
        verbose_name= 'Treasury Level 1 COA'

    def __str__(self):
        return str(self.AccountL1Code)


class L2Account(models.Model):
    AccountL2Code = models.BigIntegerField(primary_key=True, verbose_name='account l2 code')
    AccountL2LongName = models.CharField(max_length=255, verbose_name='account l2 long name', blank=True, null=True)
    AccountL1Code = models.ForeignKey(L1Account, verbose_name='account l1 code', on_delete=models.PROTECT)

    class Meta:
        verbose_name= 'Treasury Level 2 COA'

    def __str__(self):
        return str(self.AccountL2Code)


class L3Account(models.Model):
    AccountL3Code = models.BigIntegerField(verbose_name='account l3 code', primary_key=True)
    AccountL3LongName = models.CharField(max_length=255, verbose_name='account l3 long name')
    AccountL2Code = models.ForeignKey(L2Account, verbose_name='account l2 code', on_delete=models.PROTECT)

    class Meta:
        verbose_name= 'Treasury Level 3 COA'

    def __str__(self):
        return str(self.AccountL3Code)


class L4Account(models.Model):
    AccountL4Code = models.BigIntegerField(verbose_name='account l4 code', primary_key=True)
    AccountL4LongName = models.CharField(max_length=255, verbose_name='account l4 long name')
    AccountL3Code = models.ForeignKey(L3Account, verbose_name='account l3 code',on_delete=models.PROTECT)

    class Meta:
        verbose_name= 'Treasury Level 4 COA'

    def __str__(self):
        return str(self.AccountL4Code)


class L5Account(models.Model):
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
    AccountL5Code = models.BigIntegerField(primary_key=True,verbose_name='account l5 code')
    AccountL5LongName = models.CharField(max_length=255, verbose_name='account l5 long name')
    AccountL5Description = models.CharField(max_length=2048, verbose_name='account l5 description')
    AccountL4Code = models.ForeignKey(L4Account, verbose_name='account l4 code',on_delete=models.PROTECT)
    EconomicBudgetCode = models.CharField(max_length=255, verbose_name='economic budget code')
    SectorCode = models.CharField(max_length=255, verbose_name='sector code')
    EstimatesColumnCode = models.CharField(max_length=25, choices=ESTIMATECODE_CHOICES, default=UNDEF, verbose_name='estimates column code')
    UsageCode = models.CharField(max_length=25, choices=USAGECODE_CHOICES, default=BOTH, verbose_name='usage code')
    CashIndicatorCode = models.CharField(max_length=5, verbose_name='cash indicator code')

    class Meta:
        verbose_name= 'Treasury Level 5 COA'

    def __str__(self):
        return str(self.AccountL5Code)


class NACDashboardGrouping(models.Model):
    GroupingDescription = models.CharField(max_length=255, verbose_name='Description')

    def __str__(self):
        return str(self.GroupingDescription)


# define level1 values: Capital, staff, etc is Level 1 in UKTI nac hierarchy
class NaturalCode(models.Model):
    CAPITAL = 'Capital'
    STAFF = 'Staff'
    NONSTAFF = 'NonStaff'
    OTHER = 'Other'
    CATEGORY_CHOICES = (
        (CAPITAL, 'Capital'),
        (STAFF, 'Staff Cost'),
        (NONSTAFF, 'Non Staff Cost'),
        (OTHER, 'Other'),
    )
    NaturalAccountCode = models.IntegerField(primary_key=True)
    NaturalAccountDescription = models.CharField(max_length=200)
    CategoryDIT = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default=OTHER, blank=True, null=True)
    AccountL5Code = models.ForeignKey(L5Account,on_delete=models.PROTECT)
    AccountGrouping = models.ForeignKey(NACDashboardGrouping,on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return str(self.NaturalAccountCode)


class Programme(models.Model):
    ProgrammeCode = models.CharField('Programme Code', primary_key=True, max_length=50)
    ProgrammeDescription = models.CharField('Description', max_length=100)
    BudgetType = models.CharField('Budget Type', max_length=100)

    def __str__(self):
       return self.ProgrammeCode


# The ADIReport contains the forecast and the actuals
# The current month defines what is Actual and what is Forecast
class ADIReport(models.Model):

    Year = models.IntegerField()
    Programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
    CCCode = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    NaturalAccountCode = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
    Analysis1Code = models.ForeignKey(Analysis1, on_delete=models.PROTECT)
    Analysis2Code = models.ForeignKey(Analysis2, on_delete=models.PROTECT)
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

    class Meta:
        unique_together=('Year', 'Programme', 'CCCode', 'NaturalAccountCode','Analysis1Code','Analysis2Code')

    def __str__(self):
        return self.CCCode


class Budget(models.Model):
    Year = models.IntegerField()
    CCCode = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    Programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
    NaturalAccountCode = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
    Analysis1Code = models.ForeignKey(Analysis1, on_delete=models.PROTECT)
    Analysis2Code = models.ForeignKey(Analysis2, on_delete=models.PROTECT)
    Budget = models.DecimalField(max_digits=18, decimal_places=2)
    DateCreated = models.DateTimeField()
    CreatedBy = models.CharField(max_length=100)
    DateUpdated = models.DateTimeField(blank=True)
    UpdateBy = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.CCCode


# Treasury data
class SegmentGrandParent(models.Model):
    SegmentGrandParentCode = models.CharField(max_length=8, primary_key=True, verbose_name='segment grand parent code')
    SegmentGrandParentLongName = models.CharField(max_length=255, verbose_name='segment grand parent long name')

    def __str__(self):
        return self.SegmentGrandParentCode


class SegmentParent(models.Model):
    SegmentParentCode = models.CharField(max_length=8, primary_key=True,  verbose_name='segment parent code')
    SegmentParentLongName = models.CharField(max_length=255, verbose_name='segment parent long name')
    SegmentGrandParentCode = models.ForeignKey(SegmentGrandParent, on_delete=models.PROTECT)

    def __str__(self):
        return self.SegmentParentCode


class Segment(models.Model):
    SegmentCode = models.CharField(max_length=8, primary_key=True, verbose_name='segment code')
    SegmentLongName = models.CharField(max_length=255, verbose_name='segment long name')
    SegmentParentCode = models.ForeignKey(SegmentParent, on_delete=models.PROTECT)

    def __str__(self):
        return self.SegmentCode


class EstimateRow(models.Model):
    EstimatesRowCode = models.CharField(max_length=8, primary_key=True, verbose_name='estimates row code')
    EstimatesRowLongName = models.CharField(max_length=255, verbose_name='estimates row long name')

    def __str__(self):
        return self.EstimatesRowCode


class SubSegment(models.Model):
    VOTED = 'VT'
    NON_VOTED = 'NVT'
    UNDEF = 'N/A'
    CONTROL_ACCOUNTING_AUTH_CHOICES = (
        (VOTED, 'VOTED'),
        (NON_VOTED, (
            ('NON - VOTED_DEPT','NON - VOTED_DEPT'),
            ('NON-VOTED_CFER','NON-VOTED_CFER'),
            ('NON-VOTED_CF','NON-VOTED_CF'),
            ('NON-VOTED_PC','NON-VOTED_PC'),
            ('NON-VOTED_NIF', 'NON-VOTED_NIF'),
            ('NON-VOTED_NLF','NON-VOTED_NLF'),
            ('NON-VOTED_CEX','NON-VOTED_CEX'),
            ('NON-VOTED_SF','NON-VOTED_SF'),
            ('NON-VOTED_LG','NON-VOTED_LG'),
            ('NON-VOTED_DA','NON-VOTED_DA'),
         )
         ),
        (UNDEF, UNDEF),
    )

    DEL = 'DEL'
    AME = 'AME'
    NB = 'NON-BUDGET'
    DELADM = 'DEL ADMIN'
    DELPROG= 'DEL PROG'
    AMEDEPT = 'DEPT AME'
    AMENODEPT = 'NON-DEPT AME'
    CONTROL_BUDGET_CHOICES = {
        (DEL, (
                (DELADM, 'DEL ADMIN'),
                (DELPROG, 'DEL PROG'),
              )
        ),
        (AME, (
                (AMEDEPT, 'DEPT AME'),
                (AMENODEPT, 'NON-DEPT AME'),
              )
        ),
        (NB, NB),

    }
    SubSegmentCode = models.CharField(max_length=8, primary_key=True, verbose_name='sub segment code')
    SubSegmentLongName = models.CharField(max_length=255, verbose_name='sub segment long name')
    SegmentCode = models.ForeignKey(Segment, on_delete=models.PROTECT)
    ControlBudgetDetailCode = models.CharField(max_length=50, choices= CONTROL_BUDGET_CHOICES, default=NB, verbose_name='control budget detail code')
    EstimatesRowCode = models.ForeignKey(EstimateRow,  on_delete=models.PROTECT)
    NetSubheadCode = models.CharField(max_length=255, verbose_name='net subhead code')
    PolicyRingfenceCode = models.CharField(max_length=255, verbose_name='policy ringfence code')
    AccountingAuthorityCode = models.CharField(max_length=255, verbose_name='accounting authority code')
    AccountingAuthorityDetailCode = models.CharField(max_length=255, choices = CONTROL_ACCOUNTING_AUTH_CHOICES, default=UNDEF, verbose_name='accounting authority detail code')

    def __str__(self):
        return self.SubSegmentCode


# The sub segment is mapped to the combination of Programme and Cost Centre
class SubSegmentUKTIMapping(models.Model):
    SubSegCode = models.ForeignKey(SubSegment, on_delete=models.PROTECT)
    CCCode = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    Programme = models.ForeignKey(Programme, on_delete=models.PROTECT)



# salaries data

# define a choice field for this
class Grade(models.Model):
    Grade = models.CharField(primary_key=True, max_length=50)
    Order = models.IntegerField
    def __str__(self):
       return self.Grade


# Pre-calculated salary averages, used for the forecast
class SalaryMonthlyAverage(models.Model):
    AVERAGETYPE_CHOICES = (('CC', 'CostCentre'),
                           ('DIR','Directorate'),
                           ('DG','DepartmentalGroup'),)
    Grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    AverageType = models.CharField(max_length=50, choices=AVERAGETYPE_CHOICES)
    AverageBy = models.CharField(max_length=50)
    AverageValue = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return self.AverageType


# Vacancies
class VacanciesHeadCount(models.Model):
    SlotCode = models.CharField(max_length=100, primary_key=True)
    VacancyGrade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    Year = models.IntegerField()
    CCCode = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    Programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
    April = models.BooleanField()
    May = models.BooleanField()
    June = models.BooleanField()
    July = models.BooleanField()
    August = models.BooleanField()
    September = models.BooleanField()
    October = models.BooleanField()
    November = models.BooleanField()
    December = models.BooleanField()
    January = models.BooleanField()
    February = models.BooleanField()
    March = models.CharField(max_length=50)
    HRReason = models.CharField(max_length=50)  # only two values are valid

    def __str__(self):
       return self.SlotCode


class PayModelCosts(models.Model):
    GroupCode = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)
    Description = models.CharField(max_length=200)
    Year = models.IntegerField()
    April = models.DecimalField(max_digits=18, decimal_places=1)
    May = models.DecimalField(max_digits=18, decimal_places=1)
    June = models.DecimalField(max_digits=18, decimal_places=1)
    July = models.DecimalField(max_digits=18, decimal_places=1)
    August = models.DecimalField(max_digits=18, decimal_places=1)
    September = models.DecimalField(max_digits=18, decimal_places=1)
    October = models.DecimalField(max_digits=18, decimal_places=1)
    November = models.DecimalField(max_digits=18, decimal_places=1)
    December = models.DecimalField(max_digits=18, decimal_places=1)
    January = models.DecimalField(max_digits=18, decimal_places=1)
    February = models.DecimalField(max_digits=18, decimal_places=1)
    March = models.DecimalField(max_digits=18, decimal_places=1)


class PayModel(models.Model):
    GroupCode = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)
    Grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    Year = models.IntegerField()
    April = models.DecimalField(max_digits=18, decimal_places=1)
    May = models.DecimalField(max_digits=18, decimal_places=1)
    June = models.DecimalField(max_digits=18, decimal_places=1)
    July = models.DecimalField(max_digits=18, decimal_places=1)
    August = models.DecimalField(max_digits=18, decimal_places=1)
    September = models.DecimalField(max_digits=18, decimal_places=1)
    October = models.DecimalField(max_digits=18, decimal_places=1)
    November = models.DecimalField(max_digits=18, decimal_places=1)
    December = models.DecimalField(max_digits=18, decimal_places=1)
    January = models.DecimalField(max_digits=18, decimal_places=1)
    February = models.DecimalField(max_digits=18, decimal_places=1)
    March = models.DecimalField(max_digits=18, decimal_places=1)


class PayCostHeadCount(models.Model):
    StaffNumber = models.IntegerField()
    Year = models.IntegerField()
    CCCode = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    Programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
    NaturalAccountCode = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
    April = models.BooleanField()
    May = models.BooleanField()
    June = models.BooleanField()
    July = models.BooleanField()
    August = models.BooleanField()
    September = models.BooleanField()
    October = models.BooleanField()
    November = models.BooleanField()
    December = models.BooleanField()
    January = models.BooleanField()
    February = models.BooleanField()
    March = models.BooleanField()


class AdminPayModel(models.Model):
    GroupCode = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)
    Year = models.IntegerField()
    PayRise = models.DecimalField(max_digits=18, decimal_places=2)
    Vacancy = models.DecimalField(max_digits=18, decimal_places=2)
    GAE = models.DecimalField(max_digits=18, decimal_places=2)
    SCSPercent = models.DecimalField(max_digits=18, decimal_places=2)
    SCSNumber = models.DecimalField(max_digits=18, decimal_places=2)
    IndicativeBudget = models.IntegerField()


# Gift and Hospitality
class GiftsAndHospitality(models.Model):
    classification = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    GroupCode = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)
    DateOffered = models.DateTimeField()
    Venue = models.CharField(max_length=1000)
    Reason = models.CharField(max_length=1000)
    Value = models.DecimalField(max_digits=18, decimal_places=2)
    Band = models.CharField(max_length=50)
    UKTIRep = models.CharField(max_length=255)
    Offer = models.CharField(max_length=50)
    CompanyRep = models.CharField(max_length=50)
    Company = models.CharField(max_length=255)
    ActionTaken = models.CharField(max_length=50)
    DateStamp = models.DateTimeField()
    EnteredBy = models.CharField(max_length=50)
    SE_No = models.CharField(max_length=50)
    EnteredDateStamp = models.DateTimeField()
    Category = models.CharField(max_length=255)
    Grade = models.ForeignKey(Grade, on_delete=models.PROTECT)


class HotelAndTravel(models.Model):
    TravellerName = models.CharField(max_length=500)
    ProductType = models.CharField(max_length=500)
    RoomNights = models.IntegerField()
    TravelDate = models.CharField(max_length=10)
    Routing = models.CharField(max_length=500)
    GeogIndicator = models.CharField(max_length=500)
    HotelCity = models.CharField(max_length=500)
    classOfService = models.CharField(max_length=500)
    RailJourneyType = models.CharField(max_length=500)
    HotelName = models.CharField(max_length=500)
    SupplierName = models.CharField(max_length=500)
    FeePaid = models.DecimalField(max_digits=18, decimal_places=2)
    IntDom = models.CharField(max_length=500)
    ReasonCodeDesc = models.CharField(max_length=500)
    CCCode = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    Programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
    NaturalAccountCode = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)



