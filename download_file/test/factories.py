import factory

from upload_file.models import (
    FileUpload,
)


class FileUploadFactory(factory.DjangoModelFactory):

    class Meta:
        model = FileUpload
