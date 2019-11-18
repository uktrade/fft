import factory

from upload_file.models import (
    FileUpload,
    UploadPermission,
)


class FileUploadFactory(factory.DjangoModelFactory):

    class Meta:
        model = FileUpload


class UploadPermissionFactory(factory.DjangoModelFactory):

    class Meta:
        model = UploadPermission
