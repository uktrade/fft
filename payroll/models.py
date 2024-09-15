import csv
import boto3
from io import StringIO
from django.db import models

class ForcastPayroll(models.Model):
    """
    ForcastPayroll is a Django model representing the payroll forecast details.

    Attributes:
        name: A CharField representing the name, with a maximum length of 100 characters.
        nac: A CharField representing the NAC, with a maximum length of 100 characters.
        nac_description: A CharField representing the description of the NAC, with a maximum length of 100 characters.
        project_code: A CharField representing the project code, with a maximum length of 100 characters.
        programme_code: A CharField representing the programme code, with a maximum length of 100 characters.
        budget_type: A CharField representing the type of budget, with a maximum length of 100 characters.

    Meta:
        abstract: Boolean flag indicating whether the model is abstract. Set to False.
    """
    name = models.CharField(max_length=100)
    nac = models.CharField(max_length=100)
    nac_description = models.CharField(max_length=100)
    project_code = models.CharField(max_length=100)
    programme_code = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=100)

    class Meta:
        abstract = False

class EmployeePayroll(models.Model):
    """
        EmployeePayroll model stores payroll information for employees.

        Attributes:
        id : str
            Unique identifier for each employee.
        name : str
            Name of the employee.
        grade : str
            Grade of the employee.
        staff_number : str
            Staff number assigned to the employee.
        fte : Decimal
            Full-time equivalent for the employee.
        programme_code : str
            Code of the programme the employee is part of.
        budget_type : str
            Type of budget under which the employee is categorized.
        eu_non_eu : str
            Indicates whether the employee is from the EU or non-EU.
        assignment_status : str
            Current assignment status of the employee.
        current_month : str
            The current month.
        current_year : str
            The current year.
        apr : int
            Payroll data for April.
        may : int
            Payroll data for May.
        jun : int
            Payroll data for June.
        jul : int
            Payroll data for July.
        aug : int
            Payroll data for August.
        sep : int
            Payroll data for September.
        oct : int
            Payroll data for October.
        nov : int
            Payroll data for November.
        dec : int
            Payroll data for December.
        jan : int
            Payroll data for January.
        feb : int
            Payroll data for February.
        mar : int
            Payroll data for March.
        basic_pay : Decimal
            Basic pay of the employee.
        superannuation : Decimal
            Superannuation amount for the employee.
        ernic : Decimal
            Employer's National Insurance Contribution.

        Meta:
        abstract : bool
            Indicates whether the model is abstract. In this case, set to False.
    """
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    # cost_centre_code = models.CharField(max_length=100)
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
    """
    Class representing a non-employee payroll model.

    Attributes:
        id (CharField): Unique identifier for the payroll entry, serving as the primary key.
        name (CharField): Name of the individual.
        grade (CharField): Grade classification of the individual.
        staff_number (CharField): Unique staff number of the individual.
        fte (DecimalField): Full-Time Equivalent value, with a maximum of 5 digits and 2 decimal places.
        programme_code (CharField): Code indicating the associated programme.
        budget_type (CharField): Type of budget associated with the payroll entry.
        eu_non_eu (CharField): Indicator if the individual is from EU or non-EU.
        assignment_status (CharField): Status of the individual's assignment.
        person_type (CharField): Type of individual, e.g., contractor, consultant.
        current_month (CharField): The current month of the payroll entry.
        current_year (CharField): The current year of the payroll entry.
        apr (IntegerField): Payroll data for the month of April.
        may (IntegerField): Payroll data for the month of May.
        jun (IntegerField): Payroll data for the month of June.
        jul (IntegerField): Payroll data for the month of July.
        aug (IntegerField): Payroll data for the month of August.
        sep (IntegerField): Payroll data for the month of September.
        oct (IntegerField): Payroll data for the month of October.
        nov (IntegerField): Payroll data for the month of November.
        dec (IntegerField): Payroll data for the month of December.
        jan (IntegerField): Payroll data for the month of January.
        feb (IntegerField): Payroll data for the month of February.
        mar (IntegerField): Payroll data for the month of March.
        basic_pay (DecimalField): Basic pay amount, with a maximum of 10 digits and 2 decimal places.
        superannuation (DecimalField): Superannuation contribution amount, with a maximum of 10 digits and 2 decimal places.
        ernic (DecimalField): Employer's National Insurance contribution amount, with a maximum of 10 digits and 2 decimal places.

    Meta:
        abstract (bool): Indicates that this model is not abstract.
    """
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    # cost_centre_code = models.CharField(max_length=100)
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

class PayrollEntry(models.Model):
    """
    Represents a payroll entry in a Django model.

    Attributes:
    - business_unit_number: Character field to store the business unit number.
    - business_unit_name: Character field to store the business unit name.
    - cost_center_number: Character field to store the cost center number.
    - cost_center_name: Character field to store the cost center name.
    - employee_name: Character field to store the employee name.
    - employee_number: Character field to store the employee number.
    - assignment_number: Character field to store the assignment number.
    - payroll_name: Character field to store the payroll name.
    - employee_organization: Character field to store the employee's organization.
    - employee_location: Character field to store the employee's location.
    - person_type: Character field to store the type of person (e.g., employee, contractor).
    - employee_category: Character field to store the employee's category.
    - assignment_type: Character field to store the type of assignment.
    - position: Character field to store the position of the employee.
    - grade: Character field to store the grade of the employee.
    - account_code: Character field to store the account code.
    - account_name: Character field to store the account name.
    - pay_element_name: Character field to store the pay element name.
    - effective_date: Character field to store the effective date.
    - debit_amount: Character field to store the debit amount.
    - credit_amount: Character field to store the credit amount.
    - basic_pay: Character field to store the basic pay.
    - superannuation: Character field to store the superannuation information.
    - ernic: Character field to store the ERNIC information.

    Methods:
    - parse_csv: Parses a CSV file from an S3 bucket or a local file path and creates PayrollEntry objects from its rows.
       Parameters:
       - bucket_name: S3 bucket name as a string.
       - file_path: Path to the file in the S3 bucket or local file system.
       Raises:
       - Exception: If there is an error during parsing or saving the data.

    - delete_all_records: Deletes all PayrollEntry records from the database.
    """
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
    person_type =  models.CharField(max_length=100)
    employee_category =  models.CharField(max_length=100)
    assignment_type =  models.CharField(max_length=100)
    position =  models.CharField(max_length=100)
    grade =  models.CharField(max_length=100)
    account_code =  models.CharField(max_length=100)
    account_name =  models.CharField(max_length=100)
    pay_element_name =  models.CharField(max_length=100)
    effective_date =  models.CharField(max_length=100)
    debit_amount =  models.CharField(max_length=100)
    credit_amount =  models.CharField(max_length=100)
    basic_pay =  models.CharField(max_length=100)
    superannuation =  models.CharField(max_length=100)
    ernic =  models.CharField(max_length=100)

    class Meta:
        abstract = False

    def parse_csv(self, bucket_name: str, file_path: str):
        try:
            if bucket_name is not None:
                # Initialize S3 client
                s3 = boto3.client('s3')

                # Get the file from S3
                s3_object = s3.get_object(Bucket=bucket_name, Key=file_path)

                # Read the file content
                file_content = s3_object['Body'].read().decode('utf-8-sig')
            else:
                with open(file_path, 'r') as file:
                    file_content = file.read()

            # Use StringIO to read the content as a CSV
            file = StringIO(file_content)
            reader = csv.DictReader(file)

            for row in reader:
                payroll_entry = PayrollEntry(
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

                payroll_entry.save()
        except Exception as e:
            raise e

    @staticmethod
    def delete_all_records():
        PayrollEntry.objects.all().delete()

class PayrollLookup():
    """
    class PayrollLookup():

        __init__():
            Initializes a new instance of the PayrollLookup class.
            Loads the lookup table using the load_lookup_table method.

        load_lookup_table():
            Loads the lookup table from a CSV file named 'PayrollLookup.csv'.
            Reads the file content and populates the lookup_table dictionary
            with PayElementName as the key and ToolTypePayment as the value.
            Raises an exception if there is an issue reading the file.

        get_tool_type_payment(pay_element_name: str) -> str:
            Retrieves the ToolTypePayment corresponding to the given
            pay_element_name from the lookup_table dictionary.
            Returns "unknown" if the pay_element_name is not found.
    """
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
            raise e


    def get_tool_type_payment(self, pay_element_name: str) -> str:
        return self.lookup_table.get(pay_element_name, "unknown")

