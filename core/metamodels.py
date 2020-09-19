from django.db import models

from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """Base model for all models"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(
        custom_model_name=lambda x: f'SimpleHistory{x}',
        inherit=True,
    )

    class Meta:
        abstract = True


class IsActiveModel(BaseModel):
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ArchivedModel(BaseModel):
    financial_year = models.ForeignKey("core.FinancialYear",
                                       on_delete=models.PROTECT,
                                       related_name='%(app_label)s_%(class)s')
    archived = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
