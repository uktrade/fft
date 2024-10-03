import csv
from io import StringIO

import boto3
from django.db import models
from payroll.models import PayrollLookup, PayrollEntry


class HRModel(models.Model):
    group = models.CharField(max_length=255, verbose_name='group')
    directorate = models.CharField(max_length=255)
    cc = models.CharField(max_length=255)
    cc_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    se_no = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    grade = models.CharField(max_length=10)
    employee_location_city_name = models.CharField(max_length=255)
    person_type = models.CharField(max_length=255)
    assignment_status = models.CharField(max_length=255)
    appointment_status = models.CharField(max_length=255)
    working_hours = models.DecimalField(max_digits=5, decimal_places=2)
    fte = models.DecimalField(max_digits=4, decimal_places=2)  # Full-Time Equivalent
    wmi_person = models.CharField(max_length=255, blank=True, null=True)
    wmi = models.CharField(max_length=255, blank=True, null=True)
    actual_group = models.CharField(max_length=255)
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    superannuation = models.DecimalField(max_digits=10, decimal_places=2)
    ernic = models.DecimalField(max_digits=10, decimal_places=2)  # Employer's National Insurance Contribution
    total = models.DecimalField(max_digits=10, decimal_places=2)
    costing_cc = models.CharField(max_length=255)
    return_field = models.CharField(max_length=255)  # Assuming 'Return' is a field name; rename if necessary
    programme_code = models.CharField(max_length=255, blank=True, null=True)

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
                HRModel.objects.create(
                    group=row['group'],
                    directorate=row['directorate'],
                    cc=row['cc'],
                    cc_name=row['cc_name'],
                    last_name=row['last_name'],
                    first_name=row['first_name'],
                    se_no=row['se_no'],
                    salary=row['salary'],
                    grade=row['grade'],
                    employee_location_city_name=row['employee_location_city_name'],
                    person_type=row['person_type'],
                    assignment_status=row['assignment_status'],
                    appointment_status=row['appointment_status'],
                    working_hours=row['working_hours'],
                    fte=row['fte'],
                    wmi_person=row.get('wmi_person', ''),
                    wmi=row.get('wmi', ''),
                    actual_group=row['actual_group'],
                    basic_pay=row['basic_pay'],
                    superannuation=row['superannuation'],
                    ernic=row['ernic'],
                    total=row['total'],
                    costing_cc=row['costing_cc'],
                    return_field=row['return_field'],
                    programme_code=row['306162 Code']
                )
        except Exception as e:
            raise e

    def update_records_with_basic_pay_superannuation_ernic_values(self):
        payroll_records = PayrollEntry.objects.all()

        # If payroll_records is empty, return
        if not payroll_records:
            return

        hr_records = HRModel.objects.all()
        lookup = PayrollLookup()

        # For each HR record get the total debit amount (debit - credit) and then
        # get pay_element_name from the record and use it to get the tool type payment
        # using lookup.get_tool_type_payment(pay_element_name)
        #   If the tool type payment is 'Basic Pay' then add the total debit amount to the basic_pay field of the record
        #   If the tool type payment is 'Superannuation' then add the total debit amount to the superannuation field of the record
        #   If the tool type payment is 'ERNIC' then add the total debit amount to the ernic field of the record
        #   If the tool type payment is not found then log the pay_element_name as not found
        for hr_record in hr_records:
            # Iterate through the payroll records and find employee_number that matches staff_employee_number
            current_payroll_record = None
            for payroll_record in payroll_records:
                if (payroll_record.employee_number == hr_record.se_no and
                        payroll_record.cost_center_number == hr_record.cc):
                    current_payroll_record = payroll_record
                    break

            if current_payroll_record is None:
                continue

            tool_type_payment = lookup.get_tool_type_payment(current_payroll_record.pay_element_name).lower()

            if tool_type_payment == 'basic pay':
                hr_record.basic_pay += current_payroll_record.debit_amount - current_payroll_record.credit_amount
            elif tool_type_payment == 'superannuation':
                hr_record.superannuation = int(hr_record.superannuation) + int(current_payroll_record.superannuation)
            elif tool_type_payment == 'ernic':
                hr_record.ernic = int(hr_record.ernic) + int(current_payroll_record.ernic)
            else:
                # log the pay_element_name as not found
                pass

            hr_record.save()

        # For each HR record get the record.basic_pay and set record.wmi_person to 'Yes' if basic_pay is greater than 0
        # and set record.wmi_person to 'nonpayroll' if basic_pay is less than or equal to 0
        for hr_record in hr_records:
            hr_record.wmi_person = 'payroll' if hr_record.basic_pay > 0 else 'nonpayroll'
            hr_record.save()

    class Meta:
        verbose_name = "HR"
        verbose_name_plural = "HR Records"