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
