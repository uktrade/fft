from celery import shared_task

from core.myutils import (
    get_s3_file_body,
    run_anti_virus,
)

from forecast.import_actuals import upload_trial_balance_report
from forecast.import_budgets import upload_budget_from_file

from upload_file.models import FileUpload
from upload_file.utils import set_file_upload_finished


@shared_task
def process_uploaded_file(*args):
    latest_unprocessed = (
        FileUpload.objects.filter(status=FileUpload.UNPROCESSED,)
        .order_by("-created")
        .first()
    )

    if latest_unprocessed is not None:
        latest_unprocessed.status = FileUpload.ANTIVIRUS
        latest_unprocessed.save()

        # Get file body from S3
        file_body = get_s3_file_body(latest_unprocessed.document_file.name)

        # Check for viruses
        anti_virus_result = run_anti_virus(file_body,)

        if anti_virus_result["malware"]:
            latest_unprocessed.status = FileUpload.ERROR
            latest_unprocessed.user_error_message = "A virus was found in the file"
            latest_unprocessed.error_message = str(anti_virus_result)
            latest_unprocessed.save()
        else:
            latest_unprocessed.status = FileUpload.PROCESSING
            latest_unprocessed.save()

            if latest_unprocessed.document_type == FileUpload.ACTUALS:
                upload_trial_balance_report(latest_unprocessed, *args)
            if latest_unprocessed.document_type == FileUpload.BUDGET:
                upload_budget_from_file(latest_unprocessed, *args)

        set_file_upload_finished(latest_unprocessed)
