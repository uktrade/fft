import csv
from collections import namedtuple
import traceback   

from django.db import transaction
from django.db.models import Q
from django.core.files import File

from payroll.models import Employee
from costcentre.models import CostCentre
from chartofaccountDIT.models import ProgrammeCode
from gifthospitality.models import Grade

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

@transaction.atomic()
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
    cost_centre_code=[]
    programme_code=[]
    grade_id=[]
    for hr_row in hr_csv_reader:
        row=HrRow(*hr_row)
        cost_centre_code.append(row.cost_centre_id)
        programme_code.append(row.programme_code_id)
        grade_id.append(row.grade_id)
        
        validatedEmployee=hr_row_to_employee(HrRow(*hr_row))
        Employee.objects.update_or_create(employee_no=validatedEmployee["employee_no"],defaults={ **validatedEmployee})
        employees.append(validatedEmployee)
    print(set(cost_centre_code),set(grade_id),set(programme_code))
    return save_data(employees)


def hr_row_to_employee(hr_row) -> Employee:
    employee =   {
        "employee_no":hr_row.employee_no,
        "first_name":hr_row.first_name,
        "last_name":hr_row.last_name,
        "cost_centre":CostCentre.objects.get(cost_centre_code=hr_row.cost_centre_id),
        "programme_code" : ProgrammeCode.objects.get(programme_code=hr_row.programme_code_id),
        "grade":Grade.objects.get(grade=hr_row.grade_id),
        "assignment_status":hr_row.assignment_status,
        "fte":hr_row.fte,
        "basic_pay":hr_row.basic_pay,
    }
    return employee

def save_data(csv_data):
    return csv_data
    # csv_identifiers = {
    #     employee.employee_no
    #     for employee in csv_data
    # }
    # try:
    #     existing_employees = Employee.objects.all().select_for_update() 
    #     existing_identifiers = {
    #         employee.employee_no 
    #         for employee in existing_employees
    #     }

    #     left_identifiers = existing_identifiers - csv_identifiers
    #     if left_identifiers:
    #         left_filter = Q()
    #         for employee_no in left_identifiers:
    #             left_filter |= Q(
    #                 employee_no=employee_no
    #             )
    #         Employee.objects.filter(left_filter).update(has_left=True)
    #     to_create = []
    #     to_update = []
    #     for employee_from_csv in csv_data:
    #         identifier = employee_from_csv.employee_no
    #         if identifier in existing_identifiers:
    #             existing_employee = next(
    #                 emp for emp in existing_employees 
    #                 if emp.employee_no == identifier
    #             )
    #             for field in updatable_fields:
    #                 if hasattr(employee_from_csv, field):
    #                     setattr(existing_employee, field, getattr(employee_from_csv, field))
    #             existing_employee.has_left = False  
    #             to_update.append(existing_employee)
    #         else:
    #             to_create.append(employee_from_csv)
    #     Employee.objects.bulk_create(to_create)

    #     if to_update:
    #         Employee.objects.update_or_create.bulk_update( to_update,  fields=updatable_fields)
    #     return {
    #                 'created': len(to_create),
    #                 'updated': len(to_update),
    #                 'marked_left': len(left_identifiers)
    #             }
    # except Exception as e:
    #     print (traceback.format_exc())
    #     return {
    #         'status': 'error',
    #         'message': str(e),
    #         'created': 0,
    #         'updated': 0,
    #         'marked_left': 0
    #     }