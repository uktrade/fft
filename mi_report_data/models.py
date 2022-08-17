from django.db import models

from forecast.models import FinancialCode, FinancialPeriod

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
    class Meta:
        abstract = True


class ReportCurrentActualData(UniqueDataKey):
    amount = models.BigIntegerField(default=0)
    forecast = models.BigIntegerField(default=0)
    class Meta:
        managed = False
        db_table = "mi_report_current_actual"


class ReportCurrentForecastData(UniqueDataKey):
    amount = models.BigIntegerField(default=0)
    forecast = models.BigIntegerField(default=0)
    class Meta:
        managed = False
        db_table = "mi_report_current_forecast"


class UniqueDataKeyWithArchived(UniqueDataKey):
    archived_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.DO_NOTHING,
        related_name="financial_archived_period_%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True


class ReportDataView(UniqueDataKeyWithArchived):
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


class ReportPreviousMonthlyDataView(UniqueDataKeyWithArchived):
    id = models.IntegerField(primary_key=True,)
    forecast = models.BigIntegerField(default=0)
    actual = models.BigIntegerField(default=0)

    class Meta:
        abstract = True

class ReportAprDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_apr"


class ReportMayDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_may"


class ReportJunDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_jun"


class ReportJulDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_jul"


class ReportAugDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_aug"


class ReportSepDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_sep"


class ReportOctDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_oct"


class ReportNovDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_nov"


class ReportDecDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_dec"


class ReportJanDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_jan"


class ReportFebDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_feb"


class ReportMarDataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_mar"


class ReportAdj1DataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_adj1"


class ReportAdj2DataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_adj2"


class ReportAdj3DataView(ReportPreviousMonthlyDataView):
    class Meta:
        managed = False
        db_table = "mi_report_monthly_forecast_adj3"


forecast_budget_view_model = [
    # ForecastingDataView,
    ReportAprDataView,
    ReportMayDataView,
    ReportJunDataView,
    ReportJulDataView,
    ReportAugDataView,
    ReportSepDataView,
    ReportOctDataView,
    ReportNovDataView,
    ReportDecDataView,
    ReportJanDataView,
    ReportFebDataView,
    ReportMarDataView,
    ReportAdj1DataView,
    ReportAdj2DataView,
    ReportAdj3DataView,
]


class ReportBudgetArchivedData(UniqueDataKeyWithArchived):
    budget = models.BigIntegerField(default=0)
    class Meta:
        managed = False
        db_table = "mi_report_archived_budget_view"


class ReportPreviousYearDataView(UniqueDataKey):
    id = models.IntegerField(primary_key=True,)
    previous_year_actual = models.BigIntegerField(default=0)
    class Meta:
        managed = False
        db_table = "mi_report_previous_year_actual"


# # The following data are calculated using SQL.
# # They will become derived tables in Dataworkspace
# class ReportYTDView(UniqueDataKeyWithArchived):
#     ytd_budget = models.BigIntegerField(default=0)
#     ytd_actual = models.BigIntegerField(default=0)
#     class Meta:
#         managed = False
#         db_table = "mi_report_full_data"
#         default_permissions = "view"
#
#
# class ReportFullYearView(UniqueDataKeyWithArchived):
#     full_year_budget = models.BigIntegerField(default=0)
#     full_year_total = models.BigIntegerField(default=0)
#     class Meta:
#         managed = False
#         db_table = "mi_report_full_data"
#         default_permissions = "view"

