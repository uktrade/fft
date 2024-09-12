import datetime
from collections import defaultdict

from payroll.models import EmployeePayroll, NonEmployeePayroll, HR


def update_employee_tables():
    # Get all objects from HR table
    hr_objects = HR.objects.all()

    # Loop through all objects and update the employee table based on the HR record.wmi_person
    # If wmi_person is payroll, then put it in the employee table (EmployeePayroll)
    # If wmi_person is not payroll, then put it in the non-employee table (NonEmployeePayroll)
    # If the record does not exist, create it

    for hr_record in hr_objects:
        name = hr_record.first_name + " " + hr_record.last_name
        grade = hr_record.grade
        se_no = hr_record.se_no
        fte = hr_record.fte
        programme_code = hr_record.programme_code
        assignment_status = hr_record.assignment_status
        current_month = datetime.datetime.now().strftime('%B').lower()
        current_year = datetime.datetime.now().year

        if hr_record.wmi_person == "payroll":
            employee_record = EmployeePayroll()
            employee_record.name = name
            employee_record.grade = grade
            employee_record.staff_number = se_no
            employee_record.fte = fte
            employee_record.programme_code = programme_code
            employee_record.eu_non_eu = "unknown"
            employee_record.budget_type = "unknown"
            employee_record.assignment_status = assignment_status
            employee_record.current_month = current_month
            employee_record.current_year = current_year
            employee_record.save()
        elif hr_record.wmi_person == "nonpayroll":
            non_employee_record = NonEmployeePayroll()
            non_employee_record.name = name
            non_employee_record.grade = grade
            non_employee_record.staff_number = se_no
            non_employee_record.fte = fte
            non_employee_record.programme_code = programme_code
            non_employee_record.eu_non_eu = "unknown"
            non_employee_record.budget_type = "unknown"
            non_employee_record.assignment_status = assignment_status
            non_employee_record.person_type = hr_record.person_type
            non_employee_record.current_month = current_month
            non_employee_record.current_year = current_year
            non_employee_record.save()

def get_forecast_basic_pay_for_employee_non_employee_payroll() -> dict:
    # Get all objects from EmployeePayroll table
    employee_objects = EmployeePayroll.objects.all()

    # Get all objects from NonEmployeePayroll table
    non_employee_objects = NonEmployeePayroll.objects.all()

    # Loop through all objects and create a list of dictionaries for each month (april to march)
    # Each dictionary will have the following keys:
    # - month
    # - total (sum all basic_pay values for that month)

    # Initialize lists
    employee_list = []
    non_employee_list = []

    # Define the months
    months = [
        'april', 'may', 'june', 'july', 'august',
        'september', 'october', 'november', 'december',
        'january', 'february', 'march'
    ]

    # Use defaultdict to group employee and non-employee records by month
    employee_monthly_totals = defaultdict(float)
    non_employee_monthly_totals = defaultdict(float)

    # Sum the basic pay for each month for employees and non-employees
    for employee_record in employee_objects:
        employee_monthly_totals[employee_record.current_month.lower()] \
            += employee_record.basic_pay

    for non_employee_record in non_employee_objects:
        non_employee_monthly_totals[non_employee_record.current_month.lower()] \
            += non_employee_record.basic_pay

    # Build the monthly totals lists
    for month in months:
        employee_list.append({
            "month": month,
            "total": employee_monthly_totals[month]
        })
        non_employee_list.append({
            "month": month,
            "total": non_employee_monthly_totals[month]
        })

    return {
        "employee": employee_list,
        "non_employee": non_employee_list
    }
