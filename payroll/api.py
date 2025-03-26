import json
from functools import wraps

import waffle
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Router

from config import flags
from core.models import FinancialYear
from core.utils.generic_helpers import get_previous_months_data
from costcentre.models import CostCentre
from payroll.models import Employee, EmployeePayPeriods, Vacancy
from payroll.views import EditPayrollBaseView

from .services import payroll as payroll_service


router = Router()


def payroll_api(view):
    @wraps(view)
    def wrapper(request, cost_centre_code: str, financial_year: int, *args, **kwargs):
        cost_centre_obj = get_object_or_404(
            CostCentre,
            pk=cost_centre_code,
        )
        financial_year_obj = get_object_or_404(
            FinancialYear,
            pk=financial_year,
        )
        allowed = payroll_service.can_edit_payroll(
            request.user,
            cost_centre_obj,
            financial_year_obj,
            request.current_financial_year,
        )

        if not allowed:
            raise PermissionDenied

        return view(request, cost_centre_code, financial_year, *args, **kwargs)

    return wrapper


class EmployeeSchema(ModelSchema):
    class Meta:
        model = Employee
        fields = [
            "id",
            "grade",
            "employee_no",
            "fte",
            "programme_code",
            "assignment_status",
            "basic_pay",
        ]

    name: str = Field(..., alias="get_full_name")
    budget_type: str = Field(
        ...,
        alias="programme_code.budget_type.budget_type_display",
    )
    pay_periods: list[int] = Field(
        ...,
        alias="pay_periods.first.periods",
        min_length=12,
        max_length=12,
    )


@router.get("/employees/", response=list[EmployeeSchema])
@payroll_api
def get_employees(request, cost_centre_code: str, financial_year: int):
    return (
        Employee.objects.select_related(
            "programme_code__budget_type",
        )
        .prefetch_related(
            "pay_periods",
        )
        .filter(
            has_left=False,
            cost_centre_id=cost_centre_code,
            pay_periods__year=financial_year,
        )
    )


class EmployeePayPeriodsSchema(ModelSchema):
    class Meta:
        model = EmployeePayPeriods
        fields = [""]


class EditPayrollApiView(EditPayrollBaseView):
    def get(self, request, *args, **kwargs):
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
