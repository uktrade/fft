import os

from core.utils.command_helpers import CommandUpload
from import_chart_of_account.import_nac_cash_income_fields import upload_nac_fields
from upload_file.models import FileUpload


EXPECTED_EXTENSION = "xlsx"


class Command(CommandUpload):
    help = (
        "Upload the values for Cash/Non Cash and Gross/Income for the NAC."
        "It updates archived NACs, and ignore non existing NACs."
    )

    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, *args, **options):
        path = options["path"]
        _, file_extension = os.path.splitext(path)
        if file_extension.lower() != f".{EXPECTED_EXTENSION}":
            self.stdout.write(
                self.style.ERROR(f"Wrong file type {path}:" f"expected an Excel file. ")
            )
            return

        file_name = self.path_to_upload(path, EXPECTED_EXTENSION)

        fileobj = FileUpload(
            document_file_name=file_name,
            document_type=FileUpload.OTHER,
            file_location=FileUpload.LOCALFILE,
        )
        fileobj.save()
        message, success = upload_nac_fields(fileobj)
        if self.upload_s3:
            os.remove(file_name)
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))
