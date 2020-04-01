from django.contrib.auth import get_user_model
from django.db import models
from core.metamodels import BaseModel
from core.models import FinancialYear
from core.myutils import get_current_financial_year

from forecast.models import FinancialPeriod


class EndOfMonthStatus(BaseModel):
    PERIOD_CHOICES = [
        (1, 'Apr'),
        (2, 'May'),
        (3, 'Jun'),
        (4, 'Jul'),
        (5, 'Aug'),
        (6, 'Sep'),
        (7, 'Oct'),
        (8, 'Nov'),
        (9, 'Dec'),
        (10, 'Jan'),
        (11, 'Feb'),
        (12, 'Mar'),
    ]
    archived = models.BooleanField(default=False)
    archived_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    archived_period = models.IntegerField(
        max_length=11,
        choices=PERIOD_CHOICES,
    )

