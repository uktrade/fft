from chartofaccountDIT.models import Analysis1, Analysis2, NaturalCode, ProgrammeCode, ProjectCode

from core.metamodels import TimeStampedModel
from core.models import FinancialYear
from core.myutils import get_current_financial_year

from costcentre.models import CostCentre

from django.db import models

# https://github.com/martsberger/django-pivot/blob/master/django_pivot/pivot.py
from django_pivot.pivot import pivot


class FinancialPeriod(models.Model):
    """Financial periods: correspond to month, but there are 3 extra periods at the end"""
    financial_period_code = models.IntegerField(primary_key=True)  # April = 1
    period_long_name = models.CharField(max_length=20)
    period_short_name = models.CharField(max_length=10)
    period_calendar_code = models.IntegerField()  # January = 1
    # use a flag to indicate if the actuals have been uploaded instead of relying on the date
    # the actuals are manually uploaded, so it is not garanteed on which date they are uploaded
    actual_loaded = models.BooleanField(default=False)

    class Meta:
        ordering = ['financial_period_code']

    def __str__(self):
        return self.period_long_name


class FinancialCode(models.Model):
    """Contains the members of Chart of Account needed to create a unique key"""
    programme = models.ForeignKey(ProgrammeCode, on_delete=models.PROTECT)
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    natural_account_code = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
    analysis1_code = models.ForeignKey(Analysis1, on_delete=models.PROTECT, blank=True, null=True)
    analysis2_code = models.ForeignKey(Analysis2, on_delete=models.PROTECT, blank=True, null=True)
    project_code = models.ForeignKey(ProjectCode, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        abstract = True


class Budget(FinancialCode, TimeStampedModel):
    """Used to store the budgets for the financial year. The data is not profiled"""
    id = models.AutoField('Budget ID', primary_key=True)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT)
    budget = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ('programme',
                           'cost_centre',
                           'natural_account_code',
                           'analysis1_code',
                           'analysis2_code',
                           'project_code',
                           'financial_year')

    def __str__(self):
        return str(self.cost_centre) + '--' \
               + str(self.programme) + '--' \
               + str(self.natural_account_code) + '--' \
               + str(self.analysis1_code) + '--' \
               + str(self.analysis2_code) + '--' \
               + str(self.project_code) + '--' \
               + str(self.financial_year)


class PivotManager(models.Manager):
    """Managers returning the data in Monthly figures pivoted"""

    def pivotdata(self, columns={}, filter_dict={}, year=0):
        def lowercase(s):
            return s.lower()

        if year == 0:
            year = get_current_financial_year()
        if columns == {}:
            columns = {'cost_centre__cost_centre_code': 'Cost Centre Code',
                       'cost_centre__cost_centre_name': 'Cost Centre Description',
                       'natural_account_code__natural_account_code': 'Natural Account Code',
                       'natural_account_code__natural_account_code_description': 'Natural Account Code Description',
                       'programme__programme_code': 'Programme Code',
                       'programme__programme_description': 'Programme Description',
                       }
        q1 = self.get_queryset().filter(financial_year=year, **filter_dict)
        return pivot(q1,
                     columns,
                     'financial_period__period_short_name',
                     'amount', display_transform=lowercase)


class MonthlyFigure(FinancialCode, TimeStampedModel):
    """It contains the forecast and the actuals.
    The current month defines what is Actual and what is Forecast"""
    id = models.AutoField('Monthly ID', primary_key=True)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT)
    financial_period = models.ForeignKey(FinancialPeriod, on_delete=models.PROTECT)

    objects = models.Manager()  # The default manager.
    pivot = PivotManager()
    amount = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ('programme',
                           'cost_centre',
                           'natural_account_code',
                           'analysis1_code',
                           'analysis2_code',
                           'project_code',
                           'financial_year',
                           'financial_period')

    def __str__(self):
        return str(self.cost_centre) + '--' \
               + str(self.programme) + '--' \
               + str(self.natural_account_code) + '--' \
               + str(self.analysis1_code) + '--' \
               + str(self.analysis2_code) + '--' \
               + str(self.project_code) + '--' \
               + str(self.financial_year) + '--' \
               + str(self.financial_period)


class OSCARReturn(models.Model):
    """Used for downloading the Oscar return. Mapped to a view in the database, because the query is too complex"""
    # The view is created by the migration 0016_recreate_oscar_view.py
    row_number = models.BigIntegerField()
    account_l5_code = models.ForeignKey('treasuryCOA.L5Account', on_delete=models.PROTECT, db_column='account_l5_code')
    sub_segment_code = models.CharField(max_length=8, primary_key=True)
    sub_segment_long_name = models.CharField(max_length=255)
    apr = models.BigIntegerField(default=0)
    may = models.BigIntegerField(default=0)
    jun = models.BigIntegerField(default=0)
    jul = models.BigIntegerField(default=0)
    aug = models.BigIntegerField(default=0)
    sep = models.BigIntegerField(default=0)
    oct = models.BigIntegerField(default=0)
    nov = models.BigIntegerField(default=0)
    dec = models.BigIntegerField(default=0)
    jan = models.BigIntegerField(default=0)
    feb = models.BigIntegerField(default=0)
    mar = models.BigIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'forecast_oscarreturn'
        ordering = ['sub_segment_code']

# Query created in the database to return the info for the OSCAR return
# DROP VIEW "forecast_oscarreturn";
# CREATE VIEW "forecast_oscarreturn" as
#
# SELECT ROW_NUMBER () OVER (ORDER BY "treasurySS_subsegment"."sub_segment_code"),
# coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id") account_l5_code
# ,
# "treasurySS_subsegment"."sub_segment_code" , "treasurySS_subsegment"."sub_segment_long_name" ,
#
# SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Apr' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "apr", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Aug' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "aug", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Dec' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "dec", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Feb' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "feb", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jan' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "jan", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jul' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "jul", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jun' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "jun", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Mar' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "mar", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'May' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "may", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Nov' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "nov", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Oct' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "oct", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Sep' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "sep"
#
# FROM "forecast_monthlyfigure" LEFT OUTER JOIN "chartofaccountDIT_naturalcode" ON ("forecast_monthlyfigure"."natural_account_code_id" = "chartofaccountDIT_naturalcode"."natural_account_code") INNER JOIN "costcentre_costcentre" ON ("forecast_monthlyfigure"."cost_centre_id" = "costcentre_costcentre"."cost_centre_code") INNER JOIN "costcentre_directorate" ON ("costcentre_costcentre"."directorate_id" = "costcentre_directorate"."directorate_code") INNER JOIN "costcentre_departmentalgroup" ON ("costcentre_directorate"."group_id" = "costcentre_departmentalgroup"."group_code") INNER JOIN "chartofaccountDIT_programmecode" ON ("forecast_monthlyfigure"."programme_id" = "chartofaccountDIT_programmecode"."programme_code") INNER JOIN "forecast_financialperiod" ON ("forecast_monthlyfigure"."financial_period_id" = "forecast_financialperiod"."financial_period_code")
# LEFT OUTER JOIN "treasurySS_subsegment" ON ("costcentre_departmentalgroup"."treasury_segment_fk_id" = "treasurySS_subsegment"."Segment_code_id"
# AND "chartofaccountDIT_programmecode"."budget_type_fk_id" = "treasurySS_subsegment"."dit_budget_type_id")
# INNER JOIN "core_financialyear" ON ("forecast_monthlyfigure"."financial_year_id" = "core_financialyear"."financial_year")
# WHERE "core_financialyear"."current" = TRUE
# GROUP BY coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id"),
# "treasurySS_subsegment"."sub_segment_code" ;
