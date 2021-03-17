from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group,
    Permission,
)
from django.db import models

from simple_history import register

from .metamodels import (
    BaseModel,
)


class CommandLog(BaseModel):
    command_name = models.CharField(max_length=500)
    executed_at = models.DateTimeField(auto_now_add=True)
    executed_by = models.CharField(max_length=500)
    comment = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.command_name)


class FinancialPeriodManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(archived=True)
            .values(
                "financial_year",
                "financial_year_display",
            )
            .order_by("financial_year")
        )

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


class FinancialYear(BaseModel):
    """Key and representation of the financial year"""
    financial_year = models.IntegerField(primary_key=True)
    financial_year_display = models.CharField(max_length=20)
    current = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()  # The default manager.
    financial_year_objects = FinancialPeriodManager()

    def __str__(self):
        return str(self.financial_year_display)


# Track changes to permissions
register(Permission, app=__package__, inherit=True)
register(get_user_model(), app=__package__, inherit=True)
register(Group, app=__package__, inherit=True)
