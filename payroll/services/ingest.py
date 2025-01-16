import csv
from collections import namedtuple

from django.core.files import File
from django.db import DatabaseError, transaction, connection

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


@transaction.atomic
def import_payroll(
    hr_csv: File,
    # payroll_csv: File | None,
    hr_csv_has_header: bool,
    # payroll_csv_has_header: bool,
) -> str:
    hr_csv_reader = csv.reader((row.decode("utf-8") for row in hr_csv))

    if hr_csv_has_header:
        next(hr_csv_reader)

    seen_employees: set[str] = set()
    errors = []

    with connection.cursor() as cursor:
        cursor.execute("SET CONSTRAINTS ALL IMMEDIATE")

    for hr_row in hr_csv_reader:
        employee_defaults = hr_row_to_employee(HrRow(*hr_row))

        try:
            employee, _ = Employee.objects.update_or_create(
                employee_no=employee_defaults["employee_no"],
                defaults=employee_defaults,
            )
        except DatabaseError as err:
            errors.append((employee_defaults["employee_no"], str(err)))
        else:
            seen_employees.add(employee.employee_no)

    Employee.objects.exclude(employee_no__in=seen_employees).update(has_left=True)

    return {"errors": errors}


def hr_row_to_employee(hr_row) -> dict[str, object]:
    employee = {
        "employee_no": hr_row.employee_no,
        "first_name": hr_row.first_name,
        "last_name": hr_row.last_name,
        "cost_centre_id": hr_row.cost_centre_id,
        "programme_code_id": hr_row.programme_code_id,
        "grade_id": hr_row.grade_id,
        "assignment_status": hr_row.assignment_status,
        "fte": hr_row.fte,
        "basic_pay": hr_row.basic_pay,
        "has_left": False,
    }
    return employee
