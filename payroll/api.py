import json

from django.http import JsonResponse

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
        pay_modifiers = list(
            payroll_service.get_pay_modifiers_data(
                self.cost_centre,
                self.financial_year,
            )
        )

        return JsonResponse(
            {
                "employees": employees,
                "vacancies": vacancies,
                "pay_modifiers": pay_modifiers,
            }
        )

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        payroll_service.update_payroll_data(
            self.cost_centre,
            self.financial_year,
            data["employees"],
        )
        payroll_service.update_vacancies_data(
            self.cost_centre,
            self.financial_year,
            data["vacancies"],
        )
        payroll_service.update_pay_modifiers_data(
            self.cost_centre,
            self.financial_year,
            data["pay_modifiers"],
        )

        return JsonResponse({})
