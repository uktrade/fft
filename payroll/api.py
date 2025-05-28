import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from core.utils.generic_helpers import get_previous_months_data
from payroll.views import EditPayrollBaseView

from .models import Employee, Vacancy
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
        previous_months = list(get_previous_months_data(self.financial_year))
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


class EmployeesNotesApiView(EditPayrollBaseView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            if not data:
                return JsonResponse(
                    {"error": "Missing or malformed request body"}, status=400
                )

            notes = data.get("notes")
            id = data.get("id")

            if notes is None or not id:
                return JsonResponse(
                    {"error": "Both 'notes' and 'id' are required"}, status=400
                )
            get_object_or_404(Employee, id=id)
            payroll_service.update_employee_notes(
                notes,
                id,
                self.cost_centre,
                self.financial_year,
            )
            return JsonResponse({})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except ValueError:
            return JsonResponse(
                {"error": "Please check that cost centre and employee no are correct"},
                status=400,
            )


class VacanciesNotesApiView(EditPayrollBaseView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            if not data:
                return JsonResponse(
                    {"error": "Missing or malformed request body"}, status=400
                )

            notes = data.get("notes")
            id = data.get("id")

            if notes is None or not id:
                return JsonResponse(
                    {"error": "Both 'notes' and 'id' are required"}, status=400
                )
            get_object_or_404(Vacancy, id=id)
            payroll_service.update_vacancy_notes(
                notes,
                id,
                self.cost_centre,
                self.financial_year,
            )
            return JsonResponse({})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except ValueError:
            return JsonResponse(
                {"error": "Please check that cost centre and employee no are correct"},
                status=400,
            )
