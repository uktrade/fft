from django.contrib.auth import get_user_model
from django.db import models

from core.metamodels import BaseModel

from forecast.models import FinancialPeriod


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

    class Meta:
        verbose_name = "End of Month Archive Status"
        verbose_name_plural = "End of Month Archive Statuses"
        ordering = ["archived_period"]

    def __str__(self):
        return str(self.archived_period.period_long_name)
