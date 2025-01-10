import csv
import traceback
from collections import namedtuple

from django.core.files import File
from django.db import transaction

from payroll.models import Employee


# TODO: explore using pydantic for this
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
        "programme_code",
        "payroll_cost_centre_code",
        "payroll_cost_centre_matches",
    ),
)


class ImportPayrollError(Exception):
    pass


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

    errors = []

    for row in hr_csv_reader:
        try:
            employee = process_hr_csv(row)
        except ImportPayrollError as err:
            errors.append(err)

    Employee.objects.exclude(employee_no__in=employee_ids).update(has_left=True)

    return save_data(employee_ids)


def process_hr_csv(row) -> Employee:
    try:
        # csv row -> pydantic model
        hr_row = HrRow(*hr_row_raw)
    except PydanticValidationError as err:
        raise ImportPayrollError() from err

    try:
        defaults = hr_row_to_employee_dict(hr_row)
        # pydantic model -> update or create employee
        employee, employee_created = Employee.objects.update_or_create(
            defaults=defaults,
            employee_no=hr_row.cost_centre_code,
        )
    except Exception as err:
        # FIXME: handle bad rows
        print(err)
    else:
        employee_ids.append(employee.pk)

    return employee


def hr_row_to_employee_dict(hr_row: HrRow) -> dict[str, object]:
    emp = {}
    emp["employee_no"] = hr_row.employee_no
    emp["cost_centre_id"] = hr_row.cost_centre_code
    emp["fte"] = float(hr_row.fte)
    # FIXME: finish...

    return emp


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
        "has_left",
    ]
    csv_identifiers = {employee.employee_no for employee in csv_data}
    try:
        with transaction.atomic():
            existing_employees = Employee.objects.all().select_for_update()
            existing_identifiers = {
                employee.employee_no for employee in existing_employees
            }
            left_identifiers = existing_identifiers - csv_identifiers

            if left_identifiers:
                Employee.objects.filter(employee_no__in=left_identifiers).update(
                    has_left=True
                )

            to_create = []
            to_update = []
            for employee_from_csv in csv_data:
                identifier = employee_from_csv.employee_no
                if identifier in existing_identifiers:
                    existing_employee = next(
                        emp
                        for emp in existing_employees
                        if emp.employee_no == identifier
                    )
                    for field in updatable_fields:
                        if hasattr(employee_from_csv, field):
                            setattr(
                                existing_employee,
                                field,
                                getattr(employee_from_csv, field),
                            )
                    existing_employee.has_left = False
                    to_update.append(existing_employee)
                else:
                    employee_from_csv.has_left = False
                    to_create.append(employee_from_csv)
            Employee.objects.bulk_create(to_create)

            if to_update:
                Employee.objects.bulk_update(to_update, fields=updatable_fields)
            return {
                "created": len(to_create),
                "updated": len(to_update),
                "marked_left": len(left_identifiers),
            }
    except Exception as e:
        print(traceback.format_exc())
        return {
            "status": "error",
            "message": str(e),
            "created": 0,
            "updated": 0,
            "marked_left": 0,
        }
