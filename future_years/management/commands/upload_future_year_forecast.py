import os

from django.core.management.base import CommandError

from core.utils.command_helpers import (
    CommandUpload,
)
from core.utils.command_helpers import get_no_answer
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_year_display,
)

from forecast.import_budgets import upload_figure_from_file

from upload_file.models import FileUpload


class Command(CommandUpload):
    help = "Upload the forecast for a future year."

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        year = options["financial_year"]
        year_display = get_year_display(year)
        error_message = (
            f"forecast figures "
            f"for {year_display} not uploaded."
        )

        # Validate the year. It must be in the future
        current_year = get_current_financial_year()
        if year <= current_year:
            self.stdout.write(self.style.ERROR("The year must be in the future."))
            self.stdout.write(self.style.ERROR(error_message))
            return

        prompt = (
            f"All the forecast figures "
            f"for {year_display} will be overwritten.\n"
            f"This operation cannot be undone.\n"
        )

        self.stdout.write(self.style.WARNING(prompt))
        if get_no_answer():
            self.stdout.write(self.style.ERROR(error_message))
            raise CommandError(error_message)
            return

        file_name = self.path_to_upload(path, "xslx")

        fileobj = FileUpload(
            document_file_name=file_name,
            document_type=FileUpload.FORECAST,
            file_location=FileUpload.LOCALFILE,
        )
        fileobj.save()
        upload_figure_from_file(fileobj, year)
        if self.upload_s3:
            os.remove(file_name)

        self.stdout.write(self.style.SUCCESS(f"Forecast for year {year} added."))
