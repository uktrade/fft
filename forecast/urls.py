from django.urls import path

from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
    EditForecastView,
    pasted_forecast_content,
)
from forecast.views.upload_file import (
    UploadActualsView,
    UploadBudgetView,
)
from forecast.views.view_forecast.expenditure_details import (
    CostCentreExpenditureDetailsView,
    DITExpenditureDetailsView,
    DirectorateExpenditureDetailsView,
    GroupExpenditureDetailsView,
)
from forecast.views.view_forecast.forecast_summary import (
    CostCentreView,
    DITView,
    DirectorateView,
    GroupView,
)

urlpatterns = [
    path(
        "edit/<int:cost_centre_code>/",
        EditForecastView.as_view(), name="edit_forecast"
    ),
    path(
        "add/<int:cost_centre_code>/",
        AddRowView.as_view(),
        name="add_forecast_row",
    ),
    path(
        "choose-cost-centre/",
        ChooseCostCentreView.as_view(),
        name="choose_cost_centre",
    ),
    path(
        "upload-actuals/",
        UploadActualsView.as_view(),
        name="upload_actuals_file"
    ),
    path(
        "upload-budgets/",
        UploadBudgetView.as_view(),
        name="upload_budget_file"
    ),
    path(
        "dit/",
        DITView.as_view(),
        name="forecast_dit",
    ),
    path(
        "group/<group_code>/",
        GroupView.as_view(),
        name="forecast_group",
    ),
    path(
        "directorate/<directorate_code>/",
        DirectorateView.as_view(),
        name="forecast_directorate",
    ),
    path(
        "cost-centre/<cost_centre_code>/",
        CostCentreView.as_view(),
        name="forecast_cost_centre",
    ),
    path(
        "dit/<expenditure_category>/<budget_type>/",
        DITExpenditureDetailsView.as_view(),
        name="expenditure_details_dit",
    ),
    path(
        "group/<group_code>/<expenditure_category>/<budget_type>/",
        GroupExpenditureDetailsView.as_view(),
        name="expenditure_details_group",
    ),
    path(
        "directorate/<directorate_code>/<expenditure_category>/<budget_type>/",
        DirectorateExpenditureDetailsView.as_view(),
        name="expenditure_details_directorate",
    ),
    path(
        "cost-centre/<cost_centre_code>/<expenditure_category>/<budget_type>/",
        CostCentreExpenditureDetailsView.as_view(),
        name="expenditure_details_cost_centre",
    ),
    path(
        "paste-forecast/<cost_centre_code>/",
        pasted_forecast_content,
        name="paste_forecast"
    ),
]
