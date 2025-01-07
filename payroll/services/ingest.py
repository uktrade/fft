import csv
from collections import namedtuple

from django.core.files import File

from payroll.models import Employee


HrRow = namedtuple(
    "HrRow",
    (
        "group_name",
        "directorate_name",
        "cost_centre_code",
        "cost_centre_name",
        "last_name",
        "first_name",
        "employee_no",
        "salary",
        "grade",
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
        "programme_code",
        "payroll_cost_centre_code",
        "payroll_cost_centre_matches",
    ),
)


def import_payroll(
    hr_csv: File,
    payroll_csv: File | None,
    hr_csv_has_header: bool,
    payroll_csv_has_header: bool,
) -> str:
    hr_csv_reader = csv.reader((row.decode("utf-8") for row in hr_csv))

    if hr_csv_has_header:
        next(hr_csv_reader)

    employees = []

    for hr_row in hr_csv_reader:
        employees.append(hr_row_to_employee(HrRow(*hr_row)))

    # Employee.objects.bulk_create(employees)

    return f"Success: created {len(employees)}"


def hr_row_to_employee(hr_row: HrRow) -> Employee:
    employee = Employee()

    # logic here

    return employee
