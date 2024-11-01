import csv
from collections import namedtuple
from typing import TypedDict

from django.core.files import File
from django.db import transaction

from chartofaccountDIT.models import ProgrammeCode
from costcentre.models import CostCentre
from gifthospitality.models import Grade
from payroll.models import Employee


PayrollRow = namedtuple(
    "PayrollRow",
    (
        "employee_no",
        "first_name",
        "last_name",
        "cost_centre",
        "programme_code",
        "grade",
        "assignment_status",
        "fte",
        "basic_pay",
        "ernic",
        "pension",
    ),
)


EmployeeDict = dict[str, object]


class ImportPayrollReport(TypedDict):
    failed_records: list[EmployeeDict]
    created: list[EmployeeDict]
    updated: list[EmployeeDict]


@transaction.atomic()
def import_payroll(payroll_csv: File) -> ImportPayrollReport:
    csv_reader = csv.reader((row.decode("utf-8") for row in payroll_csv))

    # Skip header row.
    next(csv_reader)

    employees = []
    cost_centres = []
    programme_codes = []
    grades = []

    for row in csv_reader:
        employee = csv_row_employee_dict(PayrollRow(*row))

        employees.append(employee)
        cost_centres.append(employee["cost_centre"])
        programme_codes.append(employee["programme_code"])
        grades.append(employee["grade"])

    uniq_cost_centre_codes = set(cost_centres)
    uniq_grades = set(grades)
    uniq_programme_codes = set(programme_codes)

    cost_centers = {
        centre.cost_centre_code: centre
        for centre in CostCentre.objects.filter(
            cost_centre_code__in=uniq_cost_centre_codes
        )
    }
    cost_center_codes = [centre.cost_centre_code for centre in cost_centers.values()]

    programme_codes = {
        code.programme_code: code
        for code in ProgrammeCode.objects.filter(
            programme_code__in=uniq_programme_codes
        )
    }
    existing_programme_codes = [
        code.programme_code for code in programme_codes.values()
    ]

    grades = {
        grade.grade: grade for grade in Grade.objects.filter(grade__in=uniq_grades)
    }
    existing_grades = [grade.grade for grade in grades.values()]

    clean_records = []
    failed_records = []

    for emp in employees:
        errors = []
        if emp["cost_centre"] not in cost_center_codes:
            errors.append(f"Cost centre '{emp["cost_centre"]}' doesn't exists")
        if emp["programme_code"] not in existing_programme_codes:
            errors.append(f"Programme code '{emp["programme_code"]}' doesn't exists")
        if emp["grade"] not in existing_grades:
            errors.append(f"Grade '{emp["grade"]}' doesn't exists")
        if errors:
            emp["errors"] = errors
            failed_records.append(emp)
        else:
            emp["cost_centre"] = cost_centers[emp["cost_centre"]]
            emp["programme_code"] = programme_codes[emp["programme_code"]]
            emp["grade"] = grades[emp["grade"]]
            clean_records.append(emp)
    result = save_data(clean_records)

    return {"failed_records": failed_records, **result}


def csv_row_employee_dict(hr_row) -> EmployeeDict:
    employee = {
        "employee_no": hr_row.employee_no,
        "first_name": hr_row.first_name,
        "last_name": hr_row.last_name,
        "cost_centre": hr_row.cost_centre,
        "programme_code": hr_row.programme_code,
        "grade": hr_row.grade,
        "assignment_status": hr_row.assignment_status,
        "fte": hr_row.fte,
        "basic_pay": hr_row.basic_pay,
        "ernic": hr_row.ernic,
        "pension": hr_row.pension,
        "has_left": False,
    }
    return employee


def save_data(csv_data):
    emp_nos = {employee["employee_no"] for employee in csv_data}
    Employee.objects.exclude(employee_no__in=emp_nos).filter(has_left=False).update(
        has_left=True
    )
    return bulk_update_or_create(csv_data)


def bulk_update_or_create(data):
    if data:
        keys = list(data[0].keys())
    existing_ids = {
        emp.employee_no: emp.id
        for emp in Employee.objects.filter(
            employee_no__in=[emp["employee_no"] for emp in data]
        )
    }
    to_update = []
    to_create = []

    for item in data:
        emp = Employee(**item)
        for key in keys:
            setattr(emp, key, item[key])

        if item["employee_no"] in existing_ids:
            emp.id = existing_ids[item["employee_no"]]
            to_update.append(emp)
        else:
            to_create.append(emp)

    if to_create:
        Employee.objects.bulk_create(to_create)
    if to_update:
        Employee.objects.bulk_update(to_update, keys)

    return {"created": to_create, "updated": to_update}
