from factory.django import DjangoModelFactory

from upload_file.models import FileUpload


class FileUploadFactory(DjangoModelFactory):
    class Meta:
        model = FileUpload
