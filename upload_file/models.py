from django.contrib.auth import get_user_model
from django.db import models

from django_chunk_upload_handlers.clam_av import validate_virus_check_result

from core.metamodels import BaseModel


class FileUpload(BaseModel):
    UNPROCESSED = "unprocessed"
    PROCESSING = "processing"
    PROCESSED = "processed"
    PROCESSEDWITHERROR = "processed_error"
    PROCESSEDWITHWARNING = "processed_warning"
    PARSING = "parsing"
    ERROR = "error"
    ANTIVIRUS = "antivirus"

    STATUS_CHOICES = [
        (UNPROCESSED, "Unprocessed"),
        (ANTIVIRUS, "Checking for viruses"),
        (PROCESSEDWITHERROR, "Processed. Not uploaded, error(s) found."),
        (PROCESSEDWITHWARNING, "Processed. Uploaded, warning(s) found."),
        (PROCESSING, "Processing"),
        (PARSING, "Processing after error"),
        (PROCESSED, "Processed and uploaded."),
        (ERROR, "Fatal error."),
    ]

    ACTUALS = "actuals"
    BUDGET = "budget"
    PREVIOUSYEAR = "previousyear"

    DOCUMENT_TYPE_CHOICES = [
        (ACTUALS, "Actuals"),
        (BUDGET, "Budget"),
        (PREVIOUSYEAR, "Previous Year"),
    ]

    LOCALFILE = "local"
    S3FILE = "S3"
    document_type = models.CharField(
        max_length=100, choices=DOCUMENT_TYPE_CHOICES, default=ACTUALS,
    )
    FILE_LOCATION_CHOICE = [
        (LOCALFILE, "File system"),
        (S3FILE, "S3 Bucket"),
    ]
    file_location = models.CharField(
        max_length=100, choices=DOCUMENT_TYPE_CHOICES, default=S3FILE,
    )

    s3_document_file = models.FileField(
        max_length=1000,
        null=True,
        blank=True,
        validators=[validate_virus_check_result, ],
    )

    document_file_name = models.CharField(max_length=1000, null=True, blank=True,)

    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=UNPROCESSED,
    )
    uploading_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    user_error_message = models.TextField(null=True, blank=True,)
    user_warning_message = models.TextField(null=True, blank=True,)
    row_process_message = models.CharField(max_length=255, null=True, blank=True,)
    error_message = models.CharField(max_length=255, null=True, blank=True,)
    error_count = models.IntegerField(null=True, blank=True, default=0,)
    warning_count = models.IntegerField(null=True, blank=True, default=0,)

    @property
    def file_name(self):
        return self.s3_document_file.name

    def __str__(self):
        return "{} {} {}".format(
            self.s3_document_file.name, self.document_type, self.status,
        )

    class Meta:
        permissions = [
            ("can_upload_admin", "Can upload in Admin"),
        ]
