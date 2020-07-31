import os
import uuid

import boto3

import botocore

from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from chartofaccountDIT.import_csv import (
    import_Analysis1,
    import_Analysis2,
    import_NAC,
    import_NAC_DIT,
    import_NAC_category,
    import_NAC_expenditure_category,
    import_commercial_category,
    import_expenditure_category,
    import_programme,
)

from costcentre.import_csv import import_cc

from forecast.import_csv import (
    WrongChartOFAccountCodeException,
    import_adi_file,
)

from treasuryCOA.import_csv import import_treasury_COA

IMPORT_TYPE = {
    "CostCentre": import_cc,
    # 'Segments' : import_treasury_segments,
    "Treasury_COA": import_treasury_COA,
    "Programmes": import_programme,
    "NAC": import_NAC,  # import from the BICC file
    "Analysis1": import_Analysis1,
    "Analysis2": import_Analysis2,
    "NAC_Dashboard_Group": import_NAC_expenditure_category,
    "NAC_Dashboard_Budget": import_expenditure_category,
    "NAC_Category": import_NAC_category,
    "NAC_DIT_Setting": import_NAC_DIT,  # add extra fields defined by DIT
    "NAC_Dashboard_other": import_expenditure_category,
    "Commercial_Cat": import_commercial_category,
    "ADI": import_adi_file,
}

session = boto3.Session(
    aws_access_key_id=settings.TEMP_FILE_AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.TEMP_FILE_AWS_SECRET_ACCESS_KEY,
)

s3 = session.resource("s3")


class Command(BaseCommand):
    help = "Import data from csv file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path")
        parser.add_argument("type")
        parser.add_argument("year", type=int, nargs="?", default=None)
        parser.add_argument("month", nargs="?", default=None)

    # pass the file path as an argument
    # second argument will define the content of the file
    # importing actual is a special case, because we need to specify the month
    def handle(self, *args, **options):
        path = options.get("csv_path")
        import_type = options.get("type")

        if settings.TEMP_FILE_AWS_ACCESS_KEY_ID:
            file_name = f"{uuid.uuid4()}.csv"

            try:
                s3.Bucket(settings.TEMP_FILE_AWS_STORAGE_BUCKET_NAME).download_file(
                    path, file_name,
                )
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    print("The object does not exist.")
                else:
                    raise

            self.stdout.write(
                self.style.SUCCESS(
                    f"Downloaded file {path} from S3, " f"starting processing."
                )
            )
        else:
            file_name = path
            self.stdout.write(self.style.SUCCESS(f"Using local file {path}."))

        # Windows-1252 or CP-1252, used because of a back quote
        csv_file = open(file_name, newline="", encoding="cp1252")
        try:
            success, msg = IMPORT_TYPE[import_type](csv_file)
        except WrongChartOFAccountCodeException as ex:
            csv_file.close()

            raise CommandError(f"Failure import {import_type}: {str(ex)}")
        csv_file.close()
        if success:
            os.remove(file_name)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully completed import {import_type}.")
            )
        else:
            raise CommandError(f"Failure import {import_type}: {msg}.")
