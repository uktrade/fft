import csv
import boto3
from io import StringIO
from django.db import models
# from app_layer.log import LogService


class Payroll(models.Model):
    payroll_id = models.CharField(max_length=100, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    business_unit_number = models.CharField(max_length=100)
    business_unit_name = models.CharField(max_length=100)
    cost_center_number = models.CharField(max_length=100)
    cost_center_name = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=100)
    assignment_number = models.CharField(max_length=100)
    payroll_name = models.CharField(max_length=100)
    employee_organization = models.CharField(max_length=100)
    employee_location = models.CharField(max_length=100)
    person_type = models.CharField(max_length=100)
    employee_category = models.CharField(max_length=100)
    assignment_type = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    account_code = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    pay_element_name = models.CharField(max_length=100)
    effective_date = models.DateField()
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        abstract = False

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
                Payroll.objects.create(
                    business_unit_number=row['business_unit_number'],
                    business_unit_name=row['business_unit_name'],
                    cost_center_number=row['cost_center_number'],
                    cost_center_name=row['cost_center_name'],
                    employee_name=row['employee_name'],
                    employee_number=row['employee_number'],
                    assignment_number=row['assignment_number'],
                    payroll_name=row['payroll_name'],
                    employee_organization=row['employee_organization'],
                    employee_location=row['employee_location'],
                    person_type=row['person_type'],
                    employee_category=row['employee_category'],
                    assignment_type=row['assignment_type'],
                    position=row['position'],
                    grade=row['grade'],
                    account_code=row['account_code'],
                    account_name=row['account_name'],
                    pay_element_name=row['pay_element_name'],
                    effective_date=row['effective_date'],
                    debit_amount=row['debit_amount'],
                    credit_amount=row['credit_amount'],
                )
        except Exception as e:
            # log.exc('an error occurred while parsing the payroll CSV file', e)
            raise e


    def get_unique_rows_by_cost_center(self, cost_center_number: str):
        rows = Payroll.objects.filter(cost_center_number=cost_center_number)
        unique_rows = rows.distinct('employee_number')
        return unique_rows
