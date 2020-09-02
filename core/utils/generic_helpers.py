import datetime
from io import BytesIO

import boto3

from django.conf import settings
from django.contrib.admin.models import (
    CHANGE,
    LogEntry,
)
from django.contrib.contenttypes.models import ContentType

import requests

from core.models import FinancialYear


def get_current_financial_year():
    y = FinancialYear.objects.filter(current=True)
    if y:
        current_financial_year = y.last().financial_year
    else:
        # If there is a data problem
        # and the current year is not
        # defined, return the financial
        # year for the current date
        # The UK financial year starts
        # in April, so Jan, Feb and Mar
        # are part of the previous year
        today = datetime.datetime.now()
        current_month = today.month
        current_financial_year = today.year
        if current_month < 3 or (current_month == 4 and today.day < 5):
            # before 5th April, the financial
            # year it is one year behind the
            # calendar year
            current_financial_year -= (
                1
            )

    return current_financial_year


def get_year_display(year):
    y = FinancialYear.objects.get(financial_year=year)
    if y:
        return y.financial_year_display
    else:
        return "Invalid year"


class GetValidYear:
    regex = '2017|2018|2019|2020'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value


def get_s3_file_body(file_name):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    obj = s3.Object(
        settings.AWS_STORAGE_BUCKET_NAME,
        file_name,
    )
    data = obj.get()['Body'].read()
    # loadworkbook needs a file like object to work. BytesIO transform the stream
    return BytesIO(data)


def run_anti_virus(file_body):
    # Check file with AV web service
    if settings.IGNORE_ANTI_VIRUS:
        return {'malware': False}

    files = {"file": file_body}

    auth = (
        settings.CLAM_AV_USERNAME,
        settings.CLAM_AV_PASSWORD,
    )
    response = requests.post(
        settings.CLAM_AV_URL,
        auth=auth,
        files=files,
    )

    return response.json()


def today_string():
    today = datetime.datetime.today()
    return today.strftime("%d %b %Y")


SUB_TOTAL_CLASS = "sub-total"
TOTAL_CLASS = "mid-total"
GRAND_TOTAL_CLASS = "grand-total"


def check_empty(value):
    if value is not None and value != '':
        return value

    return None


def log_object_change(
    requesting_user_id,
    message,
    obj=None,
):
    if obj:
        content_type_id = ContentType.objects.get_for_model(
            obj
        ).pk

        LogEntry.objects.log_action(
            user_id=requesting_user_id,
            content_type_id=content_type_id,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=CHANGE,
            change_message=f"{str(obj)} {message}",
        )
    else:
        LogEntry.objects.log_action(
            user_id=requesting_user_id,
            content_type_id=None,
            object_id=None,
            object_repr="",
            action_flag=CHANGE,
            change_message=message,
        )
