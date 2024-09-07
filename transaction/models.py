import csv
from io import StringIO

import boto3
from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)
    cost_centre = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    line_description = models.TextField()
    net = models.DecimalField(max_digits=10, decimal_places=2)
    fiscal_period = models.CharField(max_length=100)
    date_of_journal = models.DateField()
    purchase_order_number = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100)
    level4_code = models.CharField(max_length=100)

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
                Transaction.objects.create(
                    transaction_id=row['transaction_id'],
                    source=row['source'],
                    entity=row['entity'],
                    cost_centre=row['cost_centre'],
                    group=row['group'],
                    account=row['account'],
                    programme=row['programme'],
                    line_description=row['line_description'],
                    net=row['net'],
                    fiscal_period=row['fiscal_period'],
                    date_of_journal=row['date_of_journal'],
                    purchase_order_number=row['purchase_order_number'],
                    supplier_name=row['supplier_name'],
                    level4_code=row['level4_code'],
                )
        except Exception as e:
            # log.exc('an error occurred while parsing the CSV file', e)
            raise e

    def __str__(self):
        return self.transaction_id