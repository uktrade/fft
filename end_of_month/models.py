from django.contrib.auth import get_user_model
from django.db import models

from core.metamodels import BaseModel
from core.models import FinancialYear

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastingDataView,
    ForecastingDataViewAbstract,
)


class ArchivedPeriodManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(archived=True)
            .values(
                "archived_period__financial_period_code",
                "archived_period__period_long_name",
            )
            .order_by("archived_period__financial_period_code")
        )

    def archived_list(self):
        return list(
            super()
            .get_queryset()
            .filter(archived=True)
            .values_list(
                "archived_period__financial_period_code",
                "archived_period__period_long_name",
            )
            .order_by("-archived_period__financial_period_code")
        )


class EndOfMonthStatus(BaseModel):
    archived = models.BooleanField(default=False)
    archived_by = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, blank=True, null=True,
    )
    archived_period = models.OneToOneField(
        FinancialPeriod,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    archived_date = models.DateTimeField(blank=True, null=True,)

    objects = models.Manager()  # The default manager.
    archived_period_objects = ArchivedPeriodManager()

    class Meta:
        verbose_name = "End of Month Archive Status"
        verbose_name_plural = "End of Month Archive Statuses"
        ordering = ["archived_period"]

    def __str__(self):
        return f"{str(self.archived_period.period_long_name)} - {self.archived}"


class MonthlyTotalBudget(BaseModel):
    # Used to store the budget for each archived month.
    # It could be calculated from the archived budget,
    # but the queries are complex and it is easier to store the total
    amount = models.BigIntegerField(default=0)  # stored in pence
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT,)
    financial_code = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    archived_status = models.ForeignKey(
        "end_of_month.EndOfMonthStatus",
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    archived_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        verbose_name = "Archived total budget"
        verbose_name_plural = "Archived total budget"
        ordering = ["archived_status"]
        unique_together = ("financial_code", "archived_status")


class PreviousMonthForecast(ForecastingDataViewAbstract):
    archived_period = models.ForeignKey(FinancialPeriod, on_delete=models.PROTECT,)

    class Meta:
        abstract = True


class PreviousAprForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_apr_view"


class PreviousMayForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_may_view"


class PreviousJunForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_jun_view"


class PreviousJulForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_jul_view"


class PreviousAugForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_aug_view"


class PreviousSepForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_sep_view"


class PreviousOctForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_oct_view"


class PreviousNovForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_nov_view"


class PreviousDecForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_dec_view"


class PreviousJanForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_jan_view"


class PreviousFebForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_feb_view"


class PreviousMarForecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_mar_view"


class PreviousAdj1Forecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_adj1_view"


class PreviousAdj2Forecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_adj2_view"


class PreviousAdj3Forecast(PreviousMonthForecast):
    class Meta:
        managed = False
        db_table = "budget_forecast_adj3_view"


forecast_budget_view_model = [
    ForecastingDataView,
    PreviousAprForecast,
    PreviousMayForecast,
    PreviousJunForecast,
    PreviousJulForecast,
    PreviousAugForecast,
    PreviousSepForecast,
    PreviousOctForecast,
    PreviousNovForecast,
    PreviousDecForecast,
    PreviousJanForecast,
    PreviousFebForecast,
    PreviousMarForecast,
    PreviousAdj1Forecast,
    PreviousAdj2Forecast,
    PreviousAdj2Forecast,
]
