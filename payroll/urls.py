from django.urls import path

from . import views


app_name = "payroll"

urlpatterns = [
    # TODO: Add choose financial year and cost centre url.
    path(
        "edit/<str:cost_centre_code>/<int:financial_year>/",
        views.edit_payroll_page,
        name="edit",
    ),
    path(
        "api/<str:cost_centre_code>/<int:financial_year>/",
        views.PayrollView.as_view(),
        name="api",
    ),
]
