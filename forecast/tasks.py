from celery import shared_task

from core.myutils import run_anti_virus

from forecast.import_actuals import (
    upload_trial_balance_report,
)

from upload_file.models import FileUpload


@shared_task
def process_uploaded_file(month, year):
    latest_unprocessed = FileUpload.objects.filter(
        status=FileUpload.UNPROCESSED,
    ).order_by('-created').first()

    if latest_unprocessed is not None:
        # Check for viruses
        print("Unprocessed file: {}".format(latest_unprocessed))
        latest_unprocessed.status = FileUpload.ANTIVIRUS
        latest_unprocessed.save()

        anti_virus_result = run_anti_virus(
            latest_unprocessed.document_file,
        )
        if anti_virus_result["malware"]:
            latest_unprocessed.status = FileUpload.ERROR
            latest_unprocessed.user_error_message = "A virus was found in the file"
            latest_unprocessed.error_message = str(anti_virus_result)
            latest_unprocessed.save()
        else:
            latest_unprocessed.status = FileUpload.PROCESSING
            latest_unprocessed.save()

            upload_trial_balance_report(
                latest_unprocessed,
                month,
                year,
            )
            # Process file here

            latest_unprocessed.status = FileUpload.PROCESSED
            latest_unprocessed.save()
            print("Saved file...")
