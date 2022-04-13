import os

from core.utils.command_helpers import (
    CommandUpload,
)

from core.remove_users import bulk_delete_users

from upload_file.models import FileUpload


class Command(CommandUpload):
    help = "Upload the Trial Balance for a specific month"

    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, *args, **options):
        path = options["path"]
        file_name = self.path_to_upload(path, "xslx")

        fileobj = FileUpload(
            document_file_name=file_name,
            document_type=FileUpload.OTHER,
            file_location=FileUpload.LOCALFILE,
        )
        fileobj.save()
        howmany = bulk_delete_users(fileobj)
        if self.upload_s3:
            os.remove(file_name)

        self.stdout.write(self.style.SUCCESS(f"Deleted {howmany} users."))
