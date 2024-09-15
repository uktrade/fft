import datetime
from collections import defaultdict
from hr.models import HRModel
from payroll.models import EmployeePayroll, NonEmployeePayroll


def update_employee_tables():
    """
    Fetches all records from the HRModel and updates the employee tables based on the `wmi_person` field.

    - If `wmi_person` equals 'payroll', a corresponding record is created in the `EmployeePayroll` table.
    - If `wmi_person` equals 'nonpayroll', a corresponding record is created in the `NonEmployeePayroll` table.
    - If a record does not exist in the target table, a new record is created.

    Attributes of each HR record such as `name`, `grade`, `staff_number`, `fte`, `programme_code`, assignment_status,
    current_month, and current_year are used to populate the respective fields in the destination table.
    """
    hr_objects = HRModel.objects.all()

    # Loop through all objects and update the employee table based on the HR record.wmi_person
    # If wmi_person is payroll, then put it in the employee table (EmployeePayroll)
    # If wmi_person is not payroll, then put it in the non-employee table (NonEmployeePayroll)
    # If the record does not exist, create it

    for hr_record in hr_objects:
        name = f'{hr_record.first_name} {hr_record.last_name}'
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

def get_forecast_basic_pay_for_employee(cost_center_code, financial_year):
    """
    Generates a forecast of basic pay, ERNIC, and superannuation for employees in a given cost center and financial year.

    Parameters:
        cost_center_code (str): The code of the cost center to filter the employees.
        financial_year (str): The financial year to filter the employee records.

    Returns:
        list: A list of dictionaries, each representing a monthly forecast. Each dictionary contains:
            - programme_description: The description of the programme.
            - nac_description: The description of the natural account code.
            - natural_account_code: The natural account code.
            - programme: The programme type.
            - cost_centre: The cost center code.
            - analysis1_code: Analysis code 1.
            - analysis2_code: Analysis code 2.
            - project_code: The project code.
            - monthly_figures: A list containing a dictionary with fields:
                - actual: A boolean indicating if the figure is actual or forecasted.
                - month: The month number.
                - amount: The total amount for the month.
                - starting_amount: The starting amount for the month.
                - archived_status: Archive status (can be None).
            - budget: The budget amount (set to 0 by default).
    """
    # Get all objects from EmployeePayroll table where cost_center_code is equal to the cost_center_code

    # employee_objects = EmployeePayroll.objects.filter(cost_center_code=cost_center_code, current_year=financial_year)
    employee_objects = EmployeePayroll.objects.all()

    # Get all objects from NonEmployeePayroll table
    non_employee_objects = NonEmployeePayroll.objects.all()

    # Loop through all objects and create a list of dictionaries for each month (april to march)
    # Each dictionary will have the following keys:
    # - month
    # - total (sum all basic_pay values for that month)

    # Initialize lists
    forecast_months = []

    # Use defaultdict to group employee and non-employee records by month
    employee_monthly_totals = defaultdict(float)
    employee_ernic_totals = defaultdict(float)
    employee_superannuation_totals = defaultdict(float)

    months = [
        "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar"
    ]

    # Sum the basic pay for each month for employees and non-employees
    for employee_record in employee_objects:
        for month in months:
            if getattr(employee_record, month) > 0:
                employee_monthly_totals[month] += int(employee_record.basic_pay)

            if getattr(employee_record, month) > 0:
                employee_ernic_totals[month] += employee_record.ernic

            if getattr(employee_record, month) > 0:
                employee_superannuation_totals[month] += employee_record.superannuation

    month_map = {
        "apr": 1, "may": 2, "jun": 3, "jul": 4, "aug": 5,
        "sep": 6, "oct": 7, "nov": 8, "dec": 9,
        "jan": 10, "feb": 11, "mar": 12
    }

    # Loop through employee_monthly_totals and create a forecast_row for each month
    for month, total in employee_monthly_totals.items():
        month_number = month_map[month]
        forecast_row = {
            {
                "programme_description": "Basic Pay",
                "nac_description": "Basic Pay",
                "natural_account_code": "0000",
                "programme": "Basic Pay",
                "cost_centre": cost_center_code,
                "analysis1_code": "0000",
                "analysis2_code": "0000",
                "project_code": "0000",
                "monthly_figures": [
                    {
                        "actual": False,
                        "month": month_number,
                        "amount": total,
                        "starting_amount": total,
                        "archived_status": None,
                    }
                ],
                "budget": 0
            }
        }
        forecast_months.append(forecast_row)

    for month, total in employee_ernic_totals.items():
        month_number = month_map[month]
        forecast_row = {
            {
                "programme_description": "ERNIC",
                "nac_description": "ERNIC",
                "natural_account_code": "0000",
                "programme": "ERNIC",
                "cost_centre": cost_center_code,
                "analysis1_code": "0000",
                "analysis2_code": "0000",
                "project_code": "0000",
                "monthly_figures": [
                    {
                        "actual": False,
                        "month": month_number,
                        "amount": total,
                        "starting_amount": total,
                        "archived_status": None,
                    }
                ],
                "budget": 0
            }
        }
        forecast_months.append(forecast_row)

    for month, total in employee_superannuation_totals.items():
        month_number = month_map[month]
        forecast_row = {
            {
                "programme_description": "Superannuation",
                "nac_description": "Superannuation",
                "natural_account_code": "0000",
                "programme": "Superannuation",
                "cost_centre": cost_center_code,
                "analysis1_code": "0000",
                "analysis2_code": "0000",
                "project_code": "0000",
                "monthly_figures": [
                    {
                        "actual": False,
                        "month": month_number,
                        "amount": total,
                        "starting_amount": total,
                        "archived_status": None,
                    }
                ],
                "budget": 0
            }
        }
        forecast_months.append(forecast_row)

    return forecast_months
