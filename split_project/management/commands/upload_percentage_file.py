import os

from core.utils.command_helpers import CommandUpload

from split_project.import_project_percentage import upload_project_percentage

from upload_file.models import FileUpload


class Command(CommandUpload):
    help = "Upload the split percentage file"

    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, *args, **options):
        path = options["path"]
        file_name = self.path_to_upload(path, "xslx")

        fileobj = FileUpload(
            document_file_name=file_name,
            document_type=FileUpload.PROJECT_PERCENTAGE,
            file_location=FileUpload.LOCALFILE,
        )
        fileobj.save()
        upload_project_percentage(fileobj)
        if self.upload_s3:
            os.remove(file_name)

        self.stdout.write(self.style.SUCCESS("Percentage uploaded."))
