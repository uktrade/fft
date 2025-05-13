from django.urls import path

from forecast.views.edit_select_cost_centre import ChooseCostCentreView
from payroll.api import (
    EditPayrollApiView,
    EmployeesNotesApiView,
    PayModifiersApiView,
    VacanciesNotesApiView,
)

from . import views


app_name = "payroll"

urlpatterns = [
    path(
        "edit/<str:cost_centre_code>/<int:financial_year>/",
        views.EditPayrollPage.as_view(),
        name="edit",
    ),
    path(
        "api/<str:cost_centre_code>/<int:financial_year>/",
        EditPayrollApiView.as_view(),
        name="api",
    ),
    path(
        "api/<str:cost_centre_code>/<int:financial_year>/vacancies/notes",
        VacanciesNotesApiView.as_view(),
        name="vacancy_notes",
    ),
    path(
        "api/<str:cost_centre_code>/<int:financial_year>/employees/notes",
        EmployeesNotesApiView.as_view(),
        name="employee_notes",
    ),
    path(
        "api/<str:cost_centre_code>/<int:financial_year>/pay_modifiers/",
        PayModifiersApiView.as_view(),
        name="api_pay_modifiers",
    ),
    path(
        "edit/choose-cost-centre/",
        ChooseCostCentreView.as_view(next_page="payroll"),
        name="choose_cost_centre",
    ),
    path(
        "edit/<str:cost_centre_code>/<int:financial_year>/vacancies/create",
        views.AddVacancyView.as_view(),
        name="add_vacancy",
    ),
    path(
        "edit/<str:cost_centre_code>/<int:financial_year>/vacancies/<int:vacancy_id>/edit",
        views.EditVacancyView.as_view(),
        name="edit_vacancy",
    ),
    path(
        "edit/<str:cost_centre_code>/<int:financial_year>/vacancies/<int:vacancy_id>/delete",
        views.DeleteVacancyView.as_view(),
        name="delete_vacancy",
    ),
    path("report", views.payroll_data_report, name="report"),
    # TODO: Remove temporary views when ready.
    path("import", views.import_payroll_page, name="import"),
]
