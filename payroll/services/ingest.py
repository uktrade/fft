import csv
from collections import defaultdict, namedtuple
from operator import attrgetter
from typing import Callable, TypedDict

from django.core.files import File
from django.db import transaction

from chartofaccountDIT.models import ProgrammeCode
from core.models import FinancialYear
from core.types import MonthIndex
from costcentre.models import CostCentre
from gifthospitality.models import Grade
from payroll.models import Employee
from payroll.services.employee import (
    employee_has_left,
    employee_joined,
    employee_rejoined,
)
from payroll.tasks import update_all_payroll_forecast


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


row_to_employee_dict: dict[str, Callable[[PayrollRow], object]] = {
    "employee_no": attrgetter("employee_no"),
    "first_name": attrgetter("first_name"),
    "last_name": attrgetter("last_name"),
    "cost_centre_id": attrgetter("cost_centre"),
    "programme_code_id": attrgetter("programme_code"),
    "grade_id": attrgetter("grade"),
    "assignment_status": attrgetter("assignment_status"),
    "fte": attrgetter("fte"),
    "basic_pay": attrgetter("basic_pay"),
    "ernic": attrgetter("ernic"),
    "pension": attrgetter("pension"),
}


class ImportPayrollReport(TypedDict):
    failed: dict[str, list[str]]
    created: int
    updated: int
    have_left: int


@transaction.atomic()
def import_payroll(
    payroll_csv: File, payroll_period: MonthIndex
) -> ImportPayrollReport:
    csv_reader = csv.reader((row.decode("utf-8") for row in payroll_csv))

    # Skip header row.
    next(csv_reader)

    employees: list[Employee] = []
    failed: dict[str, list[str]] = defaultdict(list)
    seen_employee_no_set = set()

    # Fetch current data for reference.
    previous_employees = set(Employee.objects.values_list("employee_no", flat=True))
    cost_centre_codes = set(CostCentre.objects.values_list("pk", flat=True))
    programme_codes = set(ProgrammeCode.objects.values_list("pk", flat=True))
    grades = set(Grade.objects.values_list("pk", flat=True))
    current_financial_year = FinancialYear.objects.current()

    for row in csv_reader:
        if is_row_empty(row):
            continue

        emp_dict = _csv_row_employee_dict(PayrollRow(*row))
        emp_no = emp_dict["employee_no"]

        assert isinstance(emp_no, str)

        errors = []

        if emp_dict["cost_centre_id"] not in cost_centre_codes:
            errors.append(f"Cost centre '{emp_dict["cost_centre_id"]}' doesn't exists")

        if emp_dict["programme_code_id"] not in programme_codes:
            errors.append(
                f"Programme code '{emp_dict["programme_code_id"]}' doesn't exists"
            )

        if emp_dict["grade_id"] not in grades:
            errors.append(f"Grade '{emp_dict["grade_id"]}' doesn't exists")

        if errors:
            failed[emp_no] += errors
            continue

        employees.append(Employee(**emp_dict))

        seen_employee_no_set.add(emp_dict["employee_no"])

    # Upsert
    Employee.objects.bulk_create(
        employees,
        unique_fields=["employee_no"],
        update_conflicts=True,
        update_fields=row_to_employee_dict.keys(),
    )

    created = seen_employee_no_set - previous_employees
    updated = seen_employee_no_set & previous_employees

    have_left = Employee.objects.exclude(employee_no__in=seen_employee_no_set).filter(
        has_left=False
    )
    rejoined = Employee.objects.filter(employee_no__in=updated, has_left=True)

    for employee in Employee.objects.filter(employee_no__in=created):
        employee_joined(
            employee=employee,
            year=current_financial_year,
            month=payroll_period,
        )

    for employee in have_left:
        employee_has_left(
            employee=employee,
            year=current_financial_year,
            month=payroll_period,
        )

    for employee in rejoined:
        employee_rejoined(
            employee=employee,
            year=current_financial_year,
            month=payroll_period,
        )

    # Stop template attr lookup of .items creating an empty list.
    failed.default_factory = None

    # Queue up a refresh of the whole payroll forecast.
    transaction.on_commit(
        lambda: update_all_payroll_forecast.delay(
            financial_year=current_financial_year.pk
        )
    )

    return {
        "failed": failed,
        "created": len(created),
        "updated": len(updated),
        "have_left": have_left,
    }


def _csv_row_employee_dict(hr_row) -> EmployeeDict:
    return {x: y(hr_row) for x, y in row_to_employee_dict.items()}


def is_row_empty(row):
    return not any(str(cell).strip() for cell in row)
