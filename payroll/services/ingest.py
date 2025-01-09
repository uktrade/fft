import csv
from collections import namedtuple
import traceback   

from django.db import transaction
from django.db.models import Q
from django.core.files import File

from payroll.models import Employee


HrRow = namedtuple(
    "HrRow",
    (
        "group_name",
        "directorate_name",
        "cost_centre_id",
        "cost_centre_name",
        "last_name",
        "first_name",
        "employee_no",
        "basic_pay",
        "grade_id",
        "employee_location_city_name",
        "person_type",
        "assignment_status",
        "appointment_status",
        "working_hours",
        "fte",
        "col16",
        "col17",
        "col18",
        "col19",
        "col20",
        "col21",
        "col22",
        "col23",
        "return_date",
        "col25",
        "col26",
        "col27",
        "col28",
        "col29",
        "col30",
        "col31",
        "col32",
        "col33",
        "line_manager",
        "programme_code_id",
        "payroll_cost_centre_code",
        "payroll_cost_centre_matches",
    ),
)


def import_payroll(
    hr_csv: File,
    # payroll_csv: File | None,
    hr_csv_has_header: bool,
    # payroll_csv_has_header: bool,
) -> str:
    hr_csv_reader = csv.reader((row.decode("utf-8") for row in hr_csv))

    if hr_csv_has_header:
        next(hr_csv_reader)

    employees = []

    for hr_row in hr_csv_reader:
        employees.append(hr_row_to_employee(HrRow(*hr_row)))

    return save_data(employees)


def hr_row_to_employee(hr_row: HrRow) -> Employee:
    employee = Employee()
    employee_fields = vars(employee)
    matching_fields = [field for field in hr_row._fields if field in employee_fields]
    for field in matching_fields:
        setattr(employee, field, getattr(hr_row, field))
    return employee

def save_data(csv_data):
    updatable_fields = [
         "first_name",
         "last_name",
         "cost_centre_id",
         "programme_code_id",
         "assignment_status",
         "fte",
         "grade_id",
         "basic_pay",
         "ernic",
         "pension",
         "has_left"
    ]
    csv_identifiers = {
        employee.employee_no
        for employee in csv_data
    }
    try:
        with transaction.atomic():
            existing_employees = Employee.objects.all().select_for_update() 
            existing_identifiers = {
                employee.employee_no 
                for employee in existing_employees
            }
            left_identifiers = existing_identifiers - csv_identifiers
            if left_identifiers:
                left_filter = Q()
                for employee_no in left_identifiers:
                    left_filter |= Q(
                        employee_no=employee_no
                    )
                Employee.objects.filter(left_filter).update(has_left=True)
            to_create = []
            to_update = []
            for employee_from_csv in csv_data:
                identifier = employee_from_csv.employee_no
                if identifier in existing_identifiers:
                    existing_employee = next(
                        emp for emp in existing_employees 
                        if emp.employee_no == identifier
                    )
                    for field in updatable_fields:
                        if hasattr(employee_from_csv, field):
                            setattr(existing_employee, field, getattr(employee_from_csv, field))
                    existing_employee.has_left = False  
                    to_update.append(existing_employee)
                else:
                    employee_from_csv.has_left = False  
                    to_create.append(employee_from_csv)
            Employee.objects.bulk_create(to_create)

            if to_update:
                Employee.objects.bulk_update( to_update,  fields=updatable_fields)
            return {
                        'created': len(to_create),
                        'updated': len(to_update),
                        'marked_left': len(left_identifiers)
                    }
    except Exception as e:
        print (traceback.format_exc())
        return {
            'status': 'error',
            'message': str(e),
            'created': 0,
            'updated': 0,
            'marked_left': 0
        }