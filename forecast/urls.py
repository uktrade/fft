from django.urls import path

from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
    EditForecastView,
    PublishView,
    UploadActualsView,
    pasted_forecast_content,
)
from forecast.views.view_forecast import (
    CostCentreView,
    CostClassView,  # Legacy
    DITView,
    DirectorateView,
    GroupView,
    MultiForecastView,
    PivotClassView,
    pivot_test1,
)


urlpatterns = [
    path("pivot/", PivotClassView.as_view(), name="pivot"),
    path("costcentre/", CostClassView.as_view(), name="costcentre"),
    path("pivotmulti/", MultiForecastView.as_view(), name="pivotmulti"),
    path("pivot1/", pivot_test1, name="pivot1"),
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
        "publish/",
        PublishView.as_view(),
        name="publish_forecast",
    ),
    path(
        "choose-cost-centre/",
        ChooseCostCentreView.as_view(),
        name="choose_cost_centre",
    ),
    path(
        "upload-file/",
        UploadActualsView.as_view(),
        name="upload_actuals_file"
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
        "paste-forecast/<cost_centre_code>/",
        pasted_forecast_content,
        name="paste_forecast"
    ),
]
