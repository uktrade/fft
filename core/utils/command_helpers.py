import uuid

import boto3

import botocore


from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.management.base import (
    BaseCommand,
    CommandError,
)


from core.models import CommandLog

UserModel = get_user_model()


session = boto3.Session(
    aws_access_key_id=settings.TEMP_FILE_AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.TEMP_FILE_AWS_SECRET_ACCESS_KEY,
)

s3 = session.resource("s3")


class CommandUpload(BaseCommand):
    def path_to_upload(self, path, suffix):
        if settings.TEMP_FILE_AWS_ACCESS_KEY_ID:
            self.upload_s3 = True
            file_name = f"{uuid.uuid4()}.{suffix}"

            try:
                s3.Bucket(settings.TEMP_FILE_AWS_STORAGE_BUCKET_NAME).download_file(
                    path, file_name,
                )
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    raise CommandError("The object does not exist.")
                else:
                    raise

            self.stdout.write(
                self.style.SUCCESS(
                    f"Downloaded file {path} from S3, " f"starting processing."
                )
            )
        else:
            file_name = path
            self.upload_s3 = False
            self.stdout.write(self.style.SUCCESS(f"Using local file {path}."))

        return file_name


def get_no_answer():
    answer = None
    while not answer or answer not in "yn":
        answer = input("Do you wish to proceed? [yN] ")
        if not answer:
            answer = "n"
            break
        else:
            answer = answer[0].lower()
    return answer != "y"


class CommandWithUserCheck(BaseCommand):
    """
    Augments management command logic to record the user who executed the function.
    If a user will not be provide an email to the command to use in identification,
    the command will exit.
    When using this class, implement handle_validated_user() instead of handle().
    """
    command_name = __name__
    user_validated = False

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super().create_parser(prog_name, subcommand, **kwargs)
        parser.add_argument(
            "--useremail", type=str, help="Email for validation",
        )
        return parser

    def handle_validated_user(self):
        """
        The actual logic of the command. Subclasses must implement
        this method instead of handle()
        """
        raise NotImplementedError(
            "subclasses of CommandWithUserCheck must provide "
            "a handle_validated_user() method"
        )

    def handle(self, *args, **options):
        user_email = options["useremail"]
        error_message = f"User with email '{user_email}' " \
                        f"does not exist or not authorised."
        while not user_email:
            user_email = input("Please enter your email: (exit to stop) ")

        try:
            user_obj = UserModel.objects.get(email=user_email)
        except UserModel.DoesNotExist:
            CommandLog.objects.create(
                command_name=self.command_name,
                executed_by=user_email,
                comment=f"FAILURE: User with email '{user_email}' does not exist.",
            )
            raise CommandError(error_message)

        if not user_obj.is_superuser:
            CommandLog.objects.create(
                command_name=self.command_name,
                executed_by=user_email,
                comment=f"FAILURE: User {user_email} is not superuser.",
            )
            raise CommandError(error_message)

        try:
            self.handle_user(*args, **options)
            CommandLog.objects.create(
                command_name=self.command_name,
                executed_by=user_email,
                comment="Completed successfully.",
            )

        except CommandError as ex:
            CommandLog.objects.create(
                command_name=self.command_name,
                executed_by=user_email,
                comment=f"FAILURE. Error = {ex}",
            )
            raise CommandError(ex)
