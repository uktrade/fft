from pathlib import Path

from django.contrib.auth import get_user_model
from django.db import models

from core.metamodels import (
    SimpleTimeStampedModel,
)


class FileUpload(SimpleTimeStampedModel):
    UNPROCESSED = 'unprocessed'
    DOWNLOADED = 'processed'
    ERROR = 'error'

    STATUS_CHOICES = [
        (UNPROCESSED, 'Unprocessed'),
        (DOWNLOADED, 'Processing'),
        (ERROR, 'Error'),
    ]

    OSCAR_RETURN = 'Oscar'
    FORECAST_REPORT = 'Forecast'

    DOWNLOAD_TYPE_CHOICES = [
        (OSCAR_RETURN, 'Actuals'),
        (FORECAST_REPORT, 'Budget'),
    ]

    document_type = models.CharField(
        max_length=70,
        choices=DOWNLOAD_TYPE_CHOICES,
        default=FORECAST_REPORT,
    )
    document_file = models.FileField(
        upload_to='uploaded/actuals/'
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
    uploading_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return "{} {} {}".format(
            self.document_file,
            self.document_type,
            self.status,
        )
