import os

from core.utils.command_helpers import (
    CommandUpload,
)

from forecast.import_actuals import upload_trial_balance_report

from upload_file.models import FileUpload


class Command(CommandUpload):
    help = "Upload the forecast for a future year."

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        year = options["financial_year"]
        file_name = self.path_to_upload(path, 'xslx')

        fileobj = FileUpload(
            document_file_name=file_name,
            document_type=FileUpload.FORECAST,
            file_location=FileUpload.LOCALFILE,
        )
        fileobj.save()
        upload_trial_balance_report(fileobj, year)
        if self.upload_s3:
            os.remove(file_name)

        self.stdout.write(self.style.SUCCESS(f"Forecast for year {year} added."))
