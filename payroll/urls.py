from django.urls import path

from .views import edit_payroll_page, payroll_debug_page


app_name = "payroll"

urlpatterns = [
    path(
        "edit-payroll/<str:cost_centre_code>/<int:financial_year>/",
        edit_payroll_page,
        name="edit_payroll",
    ),
    path("debug/", payroll_debug_page, name="debug"),
]
