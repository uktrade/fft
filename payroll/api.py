import json

from django.http import JsonResponse

from payroll.views import EditPayrollBaseView

from .services import payroll as payroll_service


class EditPayrollApiView(EditPayrollBaseView):
    def post_data(self, data):
        raise NotImplementedError

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
        self.post_data(
            data,
        )
        return JsonResponse({})
