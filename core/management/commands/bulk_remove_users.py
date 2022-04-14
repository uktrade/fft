import os

from core.utils.command_helpers import (
    CommandUpload,
)

from core.remove_users import bulk_delete_users

from upload_file.models import FileUpload

EXPECTED_EXTENSION = "xslx"


class Command(CommandUpload):
    help = "Upload a list of users to be removed from FFT"

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
        howmany = bulk_delete_users(fileobj)
        if self.upload_s3:
            os.remove(file_name)

        self.stdout.write(self.style.SUCCESS(f"Processed {howmany} users."))
