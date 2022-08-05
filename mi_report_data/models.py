from django.db import models

from forecast.models import FinancialCode, FinancialPeriod
# Create your models here.


# financial_code_id, budget, forecast, actual,
# financial_period_id, financial_year_id, archived_period_id
class UniqueDataKey(models.Model):
    financial_code = models.ForeignKey(
        FinancialCode,
        on_delete=models.DO_NOTHING,
        related_name="financial_code_%(app_label)s_%(class)ss",
    )
    financial_year_id = models.IntegerField()
    financial_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.DO_NOTHING,
        related_name="financial_period_%(app_label)s_%(class)ss",
    )
    archived_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.DO_NOTHING,
        related_name="financial_archived_period_%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True


class ReportDataView(UniqueDataKey):
    id = models.IntegerField(primary_key=True,)
    budget = models.BigIntegerField(default=0)
    forecast = models.BigIntegerField(default=0)
    actual = models.BigIntegerField(default=0)

    class Meta:
        managed = False
        db_table = "mi_report_full_data"
        default_permissions = "view"
        permissions = [
            ("can_view_mi_report_data", "Can view MI report data"),
        ]


class ReportPreviousYearData(UniqueDataKey):
    # This model is created for convenience
    # It stores the actual for the previous year for a given period
    # Archived data are saved in a denormalized form,
    # without the financial code, but with the explicit
    # chart of account members
    # As their value is fixed, it is convenient to store them in a table
    # to be used for the MI pipeline
    actual = models.BigIntegerField(default=0)


class ReportPreviousMonthDataView(UniqueDataKey):
    id = models.IntegerField(primary_key=True,)
    previous_month_forecast = models.BigIntegerField(default=0)
    class Meta:
        managed = False
        db_table = "mi_report_full_data"
        default_permissions = "view"


# class ReportPreviousYearDataView(UniqueDataKey):
#     id = models.IntegerField(primary_key=True,)
#     previous_year_actual = models.BigIntegerField(default=0)
#     class Meta:
#         managed = False
#         db_table = "mi_report_full_data"
#         default_permissions = "view"
#
#
# # The following data are calculated using SQL.
# # They will become derived tables in Dataworkspace
# class ReportYTDView(UniqueDataKey):
#     ytd_budget = models.BigIntegerField(default=0)
#     ytd_actual = models.BigIntegerField(default=0)
#     class Meta:
#         managed = False
#         db_table = "mi_report_full_data"
#         default_permissions = "view"
#
#
# class ReportFullYearView(UniqueDataKey):
#     full_year_budget = models.BigIntegerField(default=0)
#     full_year_total = models.BigIntegerField(default=0)
#     class Meta:
#         managed = False
#         db_table = "mi_report_full_data"
#         default_permissions = "view"



# Unpivot query
# select financial_code_id, financial_year_id, unnest( array[
# 	1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
# ]
# ) as period,
# unnest( array[apr, may, jun, jul, aug, sep, oct, nov, "dec", jan, feb, mar, adj1, adj2, adj3]) as actual
# from public.previous_years_archivedforecastdata
# where (financial_year_id + 1) in (SELECT financial_year
# 	FROM public.core_financialyear where current = true)


# CREATE MATERIALIZED VIEW last_year_financial_codes as
# SELECT p.id, cost_centre_code, natural_account_code, analysis1_code, analysis2_code, project_code, programme_code
# 	FROM public.previous_years_archivedfinancialcode p
# 	JOIN public."chartofaccountDIT_archivednaturalcode" a_nac on natural_account_code_id = a_nac.id
# 	JOIN public."chartofaccountDIT_archivedprogrammecode" a_prog on programme_id = a_prog.id
# 	JOIN public."costcentre_archivedcostcentre" a_cc on cost_centre_id = a_cc.id
# 	LEFT OUTER JOIN public."chartofaccountDIT_archivedanalysis1" a_a1 on analysis1_code_id = a_a1.id
# 	LEFT OUTER JOIN public."chartofaccountDIT_archivedanalysis2" a_a2 on analysis2_code_id = a_a2.id
# 	LEFT OUTER JOIN public."chartofaccountDIT_archivedprojectcode" a_proj on project_code_id = a_proj.id
# 	WHERE
# 	 (p.financial_year_id + 1) in (SELECT financial_year
#  	FROM public.core_financialyear where current = true)
# 	;

# CREATE VIEW
# 	map_previous_year_financial_code as
# SELECT c.id as current_code, archived_id
# 	FROM public.forecast_financialcode c LEFT OUTER JOIN public.last_year_financial_codes p
# 	on
# 	cost_centre_id  = p.cost_centre_code
#  	AND
# 	c.natural_account_code_id = p.natural_account_code
# 	AND
# 	c.programme_id  = p.programme_code
# 	AND
#  	COALESCE(c.project_code_id, '') = COALESCE(p.project_code, '')
#  	AND
# 	COALESCE(c.analysis1_code_id, '') = COALESCE(p.analysis1_code, '') AND
#  	COALESCE(c.analysis2_code_id , '') = COALESCE(p.analysis2_code, '');

# select
# financial_code_id, current_code, unnest(array[
#                                             1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
#                                         ]
#                                         ) as period,
# unnest(array[
#            apr, may, jun, jul, aug, sep, oct, nov, "dec", jan, feb, mar, adj1, adj2, adj3]) as actual
#
# from public.previous_years_archivedforecastdata
#
# JOIN
# map_previous_year_financial_code
# on
# financial_code_id = archived_id
# ;
