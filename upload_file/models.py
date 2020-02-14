from pathlib import Path

from django.contrib.auth import get_user_model
from django.db import models

from core.metamodels import (
    BaseModel,
)


class FileUpload(BaseModel):
    UNPROCESSED = 'unprocessed'
    PROCESSING = 'processing'
    PROCESSED = 'processed'
    ERROR = 'error'
    ANTIVIRUS = 'antivirus'

    STATUS_CHOICES = [
        (UNPROCESSED, 'Unprocessed'),
        (ANTIVIRUS, 'Checking for viruses'),
        (PROCESSING, 'Processing'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    ]

    ACTUALS = 'actuals'
    BUDGET = 'budget'

    DOCUMENT_TYPE_CHOICES = [
        (ACTUALS, 'Actuals'),
        (BUDGET, 'Budget'),
    ]

    document_type = models.CharField(
        max_length=7,
        choices=DOCUMENT_TYPE_CHOICES,
        default=ACTUALS,
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

    @property
    def file_name(self):
        return Path(
            self.document_file.path,
        ).name

    def __str__(self):
        return "{} {} {}".format(
            self.document_file,
            self.document_type,
            self.status,
        )
