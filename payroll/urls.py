from django.urls import path

from forecast.views.edit_select_cost_centre import ChooseCostCentreView

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
        views.EmployeeView.as_view(),
        name="api",
    ),
    path(
        "api/<str:cost_centre_code>/<int:financial_year>/vacancies/",
        views.VacancyView.as_view(),
        name="api_vacancies",
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
    path(
        "api/<str:cost_centre_code>/<int:financial_year>/pay_modifiers/",
        views.PayModifierView.as_view(),
        name="api_pay_modifiers",
    ),
]
