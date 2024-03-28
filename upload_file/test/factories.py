import factory

from upload_file.models import FileUpload


class FileUploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FileUpload
