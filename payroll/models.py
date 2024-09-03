from django.db import models


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

    def parse_csv(self, file_path):
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Payroll.objects.create(
                    payroll_id=row['payroll_id'],
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

    def __str__(self):
        return self.payroll_id
