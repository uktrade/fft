from django.contrib.auth import get_user_model
from django.db import models

from core.metamodels import (
    BaseModel,
)


class FileDownload(BaseModel):
    UNPROCESSED = 'unprocessed'
    DOWNLOADED = 'downloaded'
    ERROR = 'error'

    STATUS_CHOICES = [
        (UNPROCESSED, 'Unprocessed'),
        (DOWNLOADED, 'Downloaded'),
        (ERROR, 'Error'),
    ]

    OSCAR_RETURN = 'Oscar Return'
    MI_REPORT = 'Forecast'
    MI_PREVIOUS_YEAR_REPORT = 'Previous Year Actuals'
    MI_BUDGET_REPORT = 'Budget'

    DOWNLOAD_TYPE_CHOICES = [
        (OSCAR_RETURN, 'OSCAR Return'),
        (MI_REPORT, 'Forecast'),
        (MI_PREVIOUS_YEAR_REPORT, 'Previous Year Forecast/Actuals'),
        (MI_BUDGET_REPORT, 'Budget'),
    ]

    document_type = models.CharField(
        max_length=70,
        choices=DOWNLOAD_TYPE_CHOICES,
        default=MI_REPORT,
    )
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default=UNPROCESSED,
    )
    user_error_message = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
    )
    error_message = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    downloading_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} {}".format(
            self.document_type,
            self.status,
        )
