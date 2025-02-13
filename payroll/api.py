import json

from django.conf import settings
from django.http import JsonResponse

from core.utils.generic_helpers import get_previous_months_data
from payroll.views import EditPayrollBaseView

from .services import payroll as payroll_service


class EditPayrollApiView(EditPayrollBaseView):
    def get(self, request, *args, **kwargs):
        employees = list(
            payroll_service.get_payroll_data(
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

        if settings.PAYROLL.ENABLE_FORECAST is True:
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
