from django.urls import path

from forecast.views.edit_select_cost_centre import ChooseCostCentreView

from . import views


app_name = "payroll"

urlpatterns = [
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
        views.add_vacancy_page,
        name="add_vacancy",
    ),
    path(
        "edit/<str:cost_centre_code>/<int:financial_year>/vacancies/<int:vacancy_id>/edit",
        views.edit_vacancy_page,
        name="edit_vacancy",
    ),
    path(
        "edit/<str:cost_centre_code>/<int:financial_year>/vacancies/<int:vacancy_id>/delete",
        views.delete_vacancy_page,
        name="delete_vacancy",
    ),
]
