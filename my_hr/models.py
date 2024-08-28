from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=100, unique=True, primary_key=True)
    group = models.CharField(max_length=100)
    directorate = models.CharField(max_length=100)
    cost_centre = models.CharField(max_length=100)
    cost_centre_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    se_no = models.CharField(max_length=100, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    grade = models.CharField(max_length=100)
    employee_location_city_name = models.CharField(max_length=100)
    person_type = models.CharField(max_length=100)
    assignment_status = models.CharField(max_length=100)
    appointment_status = models.CharField(max_length=100)
    working_hours = models.DecimalField(max_digits=5, decimal_places=2)
    fte = models.DecimalField(max_digits=4, decimal_places=2)
    wmi_person = models.CharField(max_length=100)
    wmi = models.CharField(max_length=100)
    actual_group = models.CharField(max_length=100)
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    superannuation = models.DecimalField(max_digits=10, decimal_places=2)
    ernic = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    costing_cc = models.CharField(max_length=100)
    return_field = models.CharField(max_length=100)

    def __str__(self):
        return self.employee_id