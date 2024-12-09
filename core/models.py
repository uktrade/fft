from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import models
from simple_history import register

from core.constants import MONTHS

from .metamodels import BaseModel


class CommandLog(BaseModel):
    command_name = models.CharField(max_length=500)
    executed_at = models.DateTimeField(auto_now_add=True)
    executed_by = models.CharField(max_length=500)
    comment = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.command_name)


class FinancialYearManager(models.Manager):
    def archived_list(self):
        return list(
            super()
            .get_queryset()
            .filter(archived=True)
            .values_list(
                "financial_year",
                "financial_year_display",
            )
            .order_by("-financial_year")
        )

    def future_list(self):
        current_year = (
            super().get_queryset().filter(current=True).first().financial_year
        )
        return list(
            super()
            .get_queryset()
            .filter(financial_year__gt=current_year)
            .values_list(
                "financial_year",
                "financial_year_display",
            )
            .order_by("-financial_year")
        )

    def future_year_dictionary(self):
        current_year = (
            super().get_queryset().filter(current=True).first().financial_year
        )

        return (
            super()
            .get_queryset()
            .filter(financial_year__gt=current_year)
            .values(
                "financial_year",
                "financial_year_display",
            )
            .order_by("financial_year")
        )


class FinancialYearQuerySet(models.QuerySet):
    def current(self):
        return self.filter(current=True).first()

    def future(self):
        current_financial_year = self.current().financial_year
        return self.filter(financial_year__gt=current_financial_year).order_by(
            "-financial_year"
        )


class FinancialYear(BaseModel):
    """Key and representation of the financial year"""

    financial_year = models.IntegerField(primary_key=True)
    financial_year_display = models.CharField(max_length=20)
    current = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)
    objects = FinancialYearQuerySet.as_manager()
    financial_year_objects = FinancialYearManager()

    def __str__(self):
        return str(self.financial_year_display)


class PayModifiers(models.Model):
    class Meta:
        abstract = True

    @property
    def periods(self) -> list[float]:
        return [getattr(self, month) for month in MONTHS]

    financial_year = models.ForeignKey(
        FinancialYear,
        on_delete=models.PROTECT,
    )
    apr = models.FloatField(default=1.0)
    may = models.FloatField(default=1.0)
    jun = models.FloatField(default=1.0)
    jul = models.FloatField(default=1.0)
    aug = models.FloatField(default=1.0)
    sep = models.FloatField(default=1.0)
    oct = models.FloatField(default=1.0)
    nov = models.FloatField(default=1.0)
    dec = models.FloatField(default=1.0)
    jan = models.FloatField(default=1.0)
    feb = models.FloatField(default=1.0)
    mar = models.FloatField(default=1.0)


class PayUplift(PayModifiers):
    pass


class Attrition(PayModifiers):
    class Meta:
        verbose_name_plural = "attrition"

    cost_centre = models.ForeignKey(
        "costcentre.CostCentre", on_delete=models.PROTECT, null=True, blank=True
    )


# Track changes to permissions
register(Permission, app=__package__, inherit=True)
register(get_user_model(), app=__package__, inherit=True)
register(Group, app=__package__, inherit=True)
