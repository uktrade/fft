import csv
import boto3
from io import StringIO
from django.db import models

class ForcastPayroll(models.Model):
    name = models.CharField(max_length=100)
    nac = models.CharField(max_length=100)
    nac_description = models.CharField(max_length=100)
    project_code = models.CharField(max_length=100)
    programme_code = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=100)

    class Meta:
        abstract = False

class EmployeePayroll(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    staff_number = models.CharField(max_length=100)
    fte = models.DecimalField(max_digits=5, decimal_places=2)
    programme_code = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=100)
    eu_non_eu = models.CharField(max_length=100)
    assignment_status = models.CharField(max_length=100)
    current_month = models.CharField(max_length=100)
    current_year = models.CharField(max_length=100)
    apr = models.IntegerField(editable=True, verbose_name='april')
    may = models.IntegerField(editable=True, verbose_name='may')
    jun = models.IntegerField(editable=True, verbose_name='june')
    jul = models.IntegerField(editable=True, verbose_name='july')
    aug = models.IntegerField(editable=True, verbose_name='august')
    sep = models.IntegerField(editable=True, verbose_name='september')
    oct = models.IntegerField(editable=True, verbose_name='october')
    nov = models.IntegerField(editable=True, verbose_name='november')
    dec = models.IntegerField(editable=True, verbose_name='december')
    jan = models.IntegerField(editable=True, verbose_name='january')
    feb = models.IntegerField(editable=True, verbose_name='february')
    mar = models.IntegerField(editable=True, verbose_name='march')
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    superannuation = models.DecimalField(max_digits=10, decimal_places=2)
    ernic = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = False

class NonEmployeePayroll(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    staff_number = models.CharField(max_length=100)
    fte = models.DecimalField(max_digits=5, decimal_places=2)
    programme_code = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=100)
    eu_non_eu = models.CharField(max_length=100)
    assignment_status = models.CharField(max_length=100)
    person_type = models.CharField(max_length=100)
    current_month = models.CharField(max_length=100)
    current_year = models.CharField(max_length=100)
    apr = models.IntegerField(editable=True, verbose_name='april')
    may = models.IntegerField(editable=True, verbose_name='may')
    jun = models.IntegerField(editable=True, verbose_name='june')
    jul = models.IntegerField(editable=True, verbose_name='july')
    aug = models.IntegerField(editable=True, verbose_name='august')
    sep = models.IntegerField(editable=True, verbose_name='september')
    oct = models.IntegerField(editable=True, verbose_name='october')
    nov = models.IntegerField(editable=True, verbose_name='november')
    dec = models.IntegerField(editable=True, verbose_name='december')
    jan = models.IntegerField(editable=True, verbose_name='january')
    feb = models.IntegerField(editable=True, verbose_name='february')
    mar = models.IntegerField(editable=True, verbose_name='march')
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    superannuation = models.DecimalField(max_digits=10, decimal_places=2)
    ernic = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = False

class PayrollModel:
    def __init__(self, business_unit_number, business_unit_name, cost_center_number, cost_center_name, employee_name, employee_number, assignment_number, payroll_name, employee_organization, employee_location, person_type, employee_category, assignment_type, position, grade, account_code, account_name, pay_element_name, effective_date, debit_amount, credit_amount, basic_pay, superannuation, ernic):
        self.business_unit_number = business_unit_number
        self.business_unit_name = business_unit_name
        self.cost_center_number = cost_center_number
        self.cost_center_name = cost_center_name
        self.employee_name = employee_name
        self.employee_number = employee_number
        self.assignment_number = assignment_number
        self.payroll_name = payroll_name
        self.employee_organization = employee_organization
        self.employee_location = employee_location
        self.person_type = person_type
        self.employee_category = employee_category
        self.assignment_type = assignment_type
        self.position = position
        self.grade = grade
        self.account_code = account_code
        self.account_name = account_name
        self.pay_element_name = pay_element_name
        self.effective_date = effective_date
        self.debit_amount = debit_amount
        self.credit_amount = credit_amount
        self.basic_pay = basic_pay
        self.superannuation = superannuation
        self.ernic = ernic

class Payroll():
    payroll_list = []

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
                payroll = PayrollModel(
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
                    basic_pay=row['basic_pay'],
                    superannuation=row['superannuation'],
                    ernic=row['ernic']
                )
                self.payroll_list.append(payroll)
        except Exception as e:
            raise e

    def get_data_list(self):
        return self.payroll_list

class HR(models.Model):
    group = models.CharField(max_length=255)
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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.se_no})"

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
                HR.objects.create(
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
            # log.exc('an error occurred while parsing the HR CSV file', e)
            raise e

    def update_records_with_basic_pay_superannuation_ernic_values(self, payroll_records: list):
        hr_records = HR.objects.all()
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

            total_debit = current_payroll_record.debit_amount - current_payroll_record.credit_amount
            tool_type_payment = lookup.get_tool_type_payment(current_payroll_record.pay_element_name).lower()

            if tool_type_payment == 'basic pay':
                hr_record.basic_pay += total_debit
            elif tool_type_payment == 'superannuation':
                hr_record.superannuation += total_debit
            elif tool_type_payment == 'ernic':
                hr_record.ernic += total_debit
            else:
                # log the pay_element_name as not found
                pass

            hr_record.save()

        # For each HR record get the record.basic_pay and set record.wmi_person to 'Yes' if basic_pay is greater than 0
        # and set record.wmi_person to 'No' if basic_pay is less than or equal to 0
        for hr_record in hr_records:
            hr_record.wmi_person = 'payroll' if hr_record.basic_pay > 0 else 'nonpayroll'
            hr_record.save()

    class Meta:
        verbose_name = "HR"
        verbose_name_plural = "HR Records"

class PayrollLookup():
    def __init__(self):
        self.lookup_table = {}
        self.load_lookup_table()


    def load_lookup_table(self):
        try:
            # Read the file content of PayrollLookup.csv located at the current directory
            file_content = open('PayrollLookup.csv', 'r').read()

            # Use StringIO to read the content as a CSV
            file = StringIO(file_content)
            reader = csv.DictReader(file)

            for row in reader:
                self.lookup_table[row['PayElementName']] = row['ToolTypePayment']

        except Exception as e:
            # log.exc('an error occurred while loading the payroll lookup table', e)
            raise e


    def get_tool_type_payment(self, pay_element_name: str) -> str:
        return self.lookup_table.get(pay_element_name, "Not found")

