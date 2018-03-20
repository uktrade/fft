from django.db import models


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

    def __str__(self):
        return self.CCCode


class Budgets(models.Model):
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



class SegmentGrandParents(models.Model):
    SegmentGrandParentCode = models.CharField(max_length=8, primary_key=True, verbose_name='segment grand parent code')
    SegmentGrandParentLongName = models.CharField(max_length=255, verbose_name='segment grand parent long name')

    def __str__(self):
        return self.SegmentGrandParentCode


class SegmentParents(models.Model):
    SegmentParentCode = models.CharField(max_length=8, primary_key=True,  verbose_name='segment parent code')
    SegmentParentLongName = models.CharField(max_length=255, verbose_name='segment parent long name')
    SegmentGrandParentCode = models.ForeignKey(SegmentGrandParents, on_delete=models.PROTECT)

    def __str__(self):
        return self.SegmentParentCode


class Segments(models.Model):
    SegmentCode = models.CharField(max_length=8, primary_key=True, verbose_name='segment code')
    SegmentLongName = models.CharField(max_length=255, verbose_name='segment long name')
    SegmentParentCode = models.ForeignKey(SegmentParents, on_delete=models.PROTECT)

    def __str__(self):
        return self.SegmentCode


class EstimateRows(models.Model):
    EstimatesRowCode = models.CharField(max_length=8, primary_key=True, verbose_name='estimates row code')
    EstimatesRowLongName = models.CharField(max_length=255, verbose_name='estimates row long name')

    def __str__(self):
        return self.EstimatesRowCode


class SubSegments(models.Model):
    SubSegmentCode = models.CharField(max_length=8, primary_key=True, verbose_name='sub segment code')
    SubSegmentLongName = models.CharField(max_length=255, verbose_name='sub segment long name')
    SegmentCode = models.ForeignKey(Segments, on_delete=models.PROTECT)
    ControlBudgetCode = models.CharField(max_length=50, verbose_name='control budget code')
    ControlBudgetDetailCode = models.CharField(max_length=50, verbose_name='control budget detail code')
    EstimatesRowCode = models.ForeignKey(EstimateRows,  on_delete=models.PROTECT)
    NetSubheadCode = models.CharField(max_length=255, verbose_name='net subhead code')
    PolicyRingfenceCode = models.CharField(max_length=255, verbose_name='policy ringfence code')
    AccountingAuthorityCode = models.CharField(max_length=255, verbose_name='accounting authority code')
    AccountingAuthorityDetailCode = models.CharField(max_length=255, verbose_name='accounting authority detail code')

    def __str__(self):
        return self.SubSegments

# The sub segment is mapped to the combination of Programme and Cost Centre
class SubSegmentUKTIMapping(models.Model):
    SubSegCode = models.ForeignKey(SubSegments, on_delete=models.PROTECT)
    CCCode = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    Programme = models.ForeignKey(Programme, on_delete=models.PROTECT)


# Account codes from Treasury

# the following table could be normalised more, but I don't think it matters
class L1Account(models.Model):
    AccountsCode = models.CharField(max_length=8, primary_key=True, verbose_name='accounts code')
    AccountL0Code = models.CharField(max_length=8, verbose_name='account l0 code')
    AccountL1Code = models.BigIntegerField(verbose_name='account l1 code')
    AccountL1LongName = models.CharField(max_length=255, verbose_name='account l1 long name')

    def __str__(self):
        return self.AccountL1Code



class L2Account(models.Model):
    AccountL2Code = models.BigIntegerField(primary_key=True, verbose_name='account l2 code')
    AccountL2LongName = models.CharField(max_length=255, verbose_name='account l2 long name')
    AccountL1Code = models.ForeignKey(L1Account, verbose_name='account l1 code', on_delete=models.PROTECT)

    def __str__(self):
        return self.AccountL2Code


class L3Accounts(models.Model):
    AccountL3Code = models.BigIntegerField(verbose_name='account l3 code', primary_key=True)
    AccountL3LongName = models.CharField(max_length=255, verbose_name='account l3 long name')
    AccountL2Code = models.ForeignKey(L2Account, verbose_name='account l2 code')

    def __str__(self):
        return self.AccountL3Code


class L4Accounts(models.Model):
    AccountL4Code = models.BigIntegerField(verbose_name='account l4 code', primary_key=True)
    AccountL4LongName = models.CharField(max_length=255, verbose_name='account l4 long name')
    AccountL3Code = models.ForeignKey(L3Accounts, verbose_name='account l3 code')

    def __str__(self):
        return self.AccountL4Code


class L5Accounts(models.Model):
    AccountL5Code = models.BigIntegerField(verbose_name='account l5 code')
    AccountL5LongName = models.CharField(max_length=255, verbose_name='account l5 long name')
    AccountL4Code = models.ForeignKey(L4Accounts, verbose_name='account l4 code')
    AccountL5Description = models.CharField(max_length=255, verbose_name='account l5 description')
    EconomicCategoryCode = models.CharField(max_length=255, verbose_name='economic category code')
    EconomicCategoryLongName = models.CharField(max_length=255, verbose_name='economic category long name')
    EconomicGroupCode = models.CharField(max_length=255, verbose_name='economic group code')
    EconomicGroupLongName = models.CharField(max_length=255, verbose_name='economic group long name')
    EconomicRingfenceCode = models.CharField(max_length=255, verbose_name='economic ringfence code')
    EconomicRingfenceLongName = models.CharField(max_length=255, verbose_name='economic ringfence long name')
    EconomicBudgetCode = models.CharField(max_length=255, verbose_name='economic budget code')
    PESAEconomicGroupCode = models.CharField(max_length=255, verbose_name='pesa economic group code')
    SectorCode = models.CharField(max_length=255, verbose_name='sector code')
    TESCode = models.CharField(max_length=255, verbose_name='tes code')
    ESACode = models.CharField(max_length=255, verbose_name='esa code')
    ESALongName = models.CharField(max_length=255, verbose_name='esa long name')
    ESAGroupCode = models.CharField(max_length=255, verbose_name='esa group code')
    ESAGroupLongName = models.CharField(max_length=255, verbose_name='esa group long name')
    PSATCode = models.CharField(max_length=255, verbose_name='psat code')
    PSATLongName = models.CharField(max_length=255, verbose_name='psat long name')
    NationalAccountsCode = models.CharField(max_length=255, verbose_name='national accounts code')
    NationalAccountsLongName = models.CharField(max_length=255, verbose_name='national accounts long name')
    EstimatesSub_CategoryCode = models.CharField(max_length=255, verbose_name='estimates sub-category code')
    EstimatesCategoryCode = models.CharField(max_length=255, verbose_name='estimates category code')
    IncomeCategoryCode = models.CharField(max_length=255, verbose_name='income category code')
    EstimatesColumnCode = models.CharField(max_length=255, verbose_name='estimates column code')
    UsageCode = models.CharField(max_length=255, verbose_name='usage code')
    CashIndicatorCode = models.CharField(max_length=255, verbose_name='cash indicator code')

    def __str__(self):
        return self.AccountL5Code


# salaries data

# define a choice field for this
class Grades(models.Model):
    Grade = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
       return self.Grade


# Pre-calculated salary averages, used for the forecast
class SalaryMonthlyAverage(models.Model):
    AVERAGETYPE_CHOICES = (('CC', 'CostCentre'),
                           ('DIR','Directorate'),
                           ('DG','DepartmentalGroup'),)
    Grade = models.ForeignKey(Grades, on_delete=models.PROTECT)
    AverageType = models.CharField(max_length=50, choices=AVERAGETYPE_CHOICES)
    AverageBy = models.CharField(max_length=50)
    AverageValue = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return self.AverageType


# Vacancies
class VacanciesHeadCount(models.Model):
    SlotCode = models.CharField(max_length=100, primary_key=True)
    VacancyGrade = models.ForeignKey(Grades, on_delete=models.PROTECT)
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
    Grade = models.ForeignKey(Grades, on_delete=models.PROTECT)
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
    Grade = models.ForeignKey(Grades, on_delete=models.PROTECT)


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



