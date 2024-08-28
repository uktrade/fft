from django.db import models


class Payroll(models.Model):
    payroll_id = models.CharField(max_length=100, unique=True, primary_key=True)
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

    def __str__(self):
        return self.payroll_id
