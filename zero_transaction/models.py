import csv
import boto3
from io import StringIO
from django.db import models
# from app_layer.log import LogService


class ZeroTransaction(models.Model):
    entity = models.CharField(max_length=100)
    cost_centre = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    analysis_1 = models.CharField(max_length=100)
    spare_1 = models.CharField(max_length=100, blank=True, null=True)
    spare_2 = models.CharField(max_length=100, blank=True, null=True)

    apr = models.FloatField()
    may = models.FloatField()
    jun = models.FloatField()
    jul = models.FloatField()
    aug = models.FloatField()
    sep = models.FloatField()
    oct = models.FloatField()
    nov = models.FloatField()
    dec = models.FloatField()
    jan = models.FloatField()
    feb = models.FloatField()
    mar = models.FloatField()

    adj1 = models.FloatField(blank=True, null=True)
    adj2 = models.FloatField(blank=True, null=True)
    adj3 = models.FloatField(blank=True, null=True)

    total = models.FloatField()

    def parse_csv(self, bucket_name: str, file_path: str):
        try:
            # Initialize S3 client
            s3 = boto3.client('s3')

            # Get the file from S3
            s3_object = s3.get_object(Bucket=bucket_name, Key=file_path)

            # Read the file content
            file_content = s3_object['Body'].read().decode('utf-8-sig')

            # Use StringIO to read the content as a CSV
            file = StringIO(file_content)
            reader = csv.DictReader(file)

            for row in reader:
                ZeroTransaction.objects.create(
                    entity=row['entity'],
                    cost_centre=row['cost_centre'],
                    account=row['account'],
                    programme=row['programme'],
                    analysis_1=row['analysis_1'],
                    spare_1=row.get('spare_1', ''),
                    spare_2=row.get('spare_2', ''),
                    apr=row['apr'],
                    may=row['may'],
                    jun=row['jun'],
                    jul=row['jul'],
                    aug=row['aug'],
                    sep=row['sep'],
                    oct=row['oct'],
                    nov=row['nov'],
                    dec=row['dec'],
                    jan=row['jan'],
                    feb=row['feb'],
                    mar=row['mar'],
                    adj1=row.get('adj1', ''),
                    adj2=row.get('adj2', ''),
                    adj3=row.get('adj3', ''),
                    total=row['total'],
                )
        except Exception as e:
            # log.exc('an error occurred while parsing the CSV file', e)
            raise e

    class Meta:
        verbose_name_plural = "Zero Transaction Entries"

    def __str__(self):
        return f"{self.entity} - {self.cost_centre} - {self.account}"

