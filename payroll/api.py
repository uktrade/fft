import json

import waffle
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from config import flags
from core.utils.generic_helpers import get_previous_months_data
from payroll.views import EditPayrollBaseView

from .services import payroll as payroll_service


class EditPayrollApiView(EditPayrollBaseView):
    def get(self, request, *args, **kwargs):

        employees = list(
            payroll_service.get_employee_data(
                self.cost_centre,
                self.financial_year,
            )
        )

        vacancies = list(
            payroll_service.get_vacancies_data(
                self.cost_centre,
                self.financial_year,
            )
        )
        pay_modifiers = payroll_service.get_pay_modifiers_data(
            self.cost_centre,
            self.financial_year,
        )

        forecast = list(
            payroll_service.payroll_forecast_report(
                self.cost_centre, self.financial_year
            )
        )
        previous_months = list(get_previous_months_data())
        actuals = payroll_service.get_actuals_data(
            self.cost_centre, self.financial_year
        )

        return JsonResponse(
            {
                "employees": employees,
                "vacancies": vacancies,
                "pay_modifiers": pay_modifiers,
                "forecast": forecast,
                "previous_months": previous_months,
                "actuals": actuals,
            }
        )

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        payroll_service.update_employee_data(
            self.cost_centre,
            self.financial_year,
            data["employees"],
        )
        payroll_service.update_vacancies_data(
            self.cost_centre,
            self.financial_year,
            data["vacancies"],
        )
        if data["pay_modifiers"]["attrition"]:
            payroll_service.update_attrition_data(
                self.cost_centre,
                self.financial_year,
                data["pay_modifiers"]["attrition"],
            )

        if waffle.switch_is_active(flags.PAYROLL):
            payroll_service.update_payroll_forecast(
                financial_year=self.financial_year,
                cost_centre=self.cost_centre,
            )

        return JsonResponse({})


class PayModifiersApiView(EditPayrollBaseView):
    def post(self, request, *args, **kwargs):
        payroll_service.create_default_pay_modifiers(
            self.cost_centre,
            self.financial_year,
        )

        return JsonResponse({})


class EmployeeNotesApi(EditPayrollBaseView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            if not data:
                return JsonResponse({"error": "Missing request body"}, status=400)
            notes = data.get("notes")
            employee_no = data.get("employee_no")

            if not notes or not employee_no:
                return JsonResponse(
                    {"error": "Both 'notes' and 'employee_no' are required"}, status=400
                )
            employee_data = payroll_service.get_employee_data(
                self.cost_centre,
                self.financial_year,
            )
            employee = next(
                (
                    item
                    for item in employee_data
                    if str(item["employee_no"]) == employee_no
                ),
                None,
            )
            if employee:
                payroll_service.update_employee_notes(
                    notes,
                    employee_no,
                    self.cost_centre,
                    self.financial_year,
                )
            return JsonResponse({}, status=204)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except ValidationError:
            return JsonResponse({"error": "Invalid data provided"}, status=400)
        except Exception:
            return JsonResponse(
                {"error": "An error occurred while processing the request"}, status=500
            )
