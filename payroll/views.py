from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Payroll

def payroll_list(request):
    return render(request, 'payroll/list/list.html')

def payroll_edit(request):
    return render(request, 'payroll/edit/edit.html')

class EditPayrollView(TemplateView):
    template_name = 'payroll/edit/edit.html'

    def get_payroll_data(self):
        # Fetch payroll data logic here
        return Payroll.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payroll_data'] = self.get_payroll_data()
        return context