from django.urls import path
from . import views
from .edit_payroll import EditPayrollView, EditPayrollUpdatesView
from .edit_select_cost_centre import SelectCostCentreView

urlpatterns = [
    path('list/',
         views.payroll_list,
         name='payroll_list'),
    path("edit/select-cost-centre/",
         SelectCostCentreView.as_view(),
         name="select_cost_centre"),
    path("edit/<int:cost_centre_code>/<int:financial_year>/",
         EditPayrollView.as_view(),
         name="edit_payroll"),
    # Path that takes the updated payroll data with cost centre code and financial year as parameters
    path("paste-payroll/<int:cost_centre_code>/<int:financial_year>",
         EditPayrollUpdatesView.as_view(),
         name="paste_payroll"),
]