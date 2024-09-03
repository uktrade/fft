import csv
from django.db import models


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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.se_no})"
    
    def parse_csv(self, file_path):
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
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
                    return_field=row['return_field']
                )
    class Meta:
        verbose_name = "HR"
        verbose_name_plural = "HR Records"
