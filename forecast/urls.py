from django.urls import path

from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
    EditForecastView,
    pasted_forecast_content,
    update_forecast_figure,
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
from forecast.views.view_forecast.programme_details import (
    DITProgrammeDetailsView,
    DirectorateProgrammeDetailsView,
    GroupProgrammeDetailsView,
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

    #         dit-programme/310530/6/
    path(
        "dit-programme/<programme_code>/<forecast_expenditure_type>/",
        DITProgrammeDetailsView.as_view(),
        name="programme_details_dit",
    ),

    #  group-programme/1090HT/310530/6/
    path(
        "group-programme/<group_code>/<programme_code>/<forecast_expenditure_type>/",
        GroupProgrammeDetailsView.as_view(),
        name="programme_details_group",
    ),

    #  directorate-programme/10907T/310530/6/
    path(
        "directorate-programme/<directorate_code>/<programme_code>/<forecast_expenditure_type>/",  # noqa
        DirectorateProgrammeDetailsView.as_view(),
        name="programme_details_directorate",
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
        "paste-forecast/<cost_centre_code>/",
        pasted_forecast_content,
        name="paste_forecast"
    ),
    path(
        "update-forecast/<cost_centre_code>/",
        update_forecast_figure,
        name="update_forecast_figure"
    ),
]
