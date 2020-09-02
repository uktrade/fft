import uuid

import boto3

import botocore


from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)


session = boto3.Session(
    aws_access_key_id=settings.TEMP_FILE_AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.TEMP_FILE_AWS_SECRET_ACCESS_KEY,
)

s3 = session.resource('s3')


class CommandUpload(BaseCommand):
    def path_to_upload(self, path, suffix):
        if settings.TEMP_FILE_AWS_ACCESS_KEY_ID:
            self.upload_s3 = True
            file_name = f"{uuid.uuid4()}.{suffix}"

            try:
                s3.Bucket(settings.TEMP_FILE_AWS_STORAGE_BUCKET_NAME).download_file(
                    path,
                    file_name,
                )
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    raise CommandError("The object does not exist.")
                else:
                    raise

            self.stdout.write(
                self.style.SUCCESS(f"Downloaded file {path} from S3, "
                                   f"starting processing.")
            )
        else:
            file_name = path
            self.upload_s3 = False
            self.stdout.write(
                self.style.SUCCESS(f"Using local file {path}.")
            )

        return file_name
