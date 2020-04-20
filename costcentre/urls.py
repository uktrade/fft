from django.urls import path

from .views import (
    FilteredCostListView,
    HistoricalFilteredCostListView,
)

urlpatterns = [
    path(
        "costcentrefilter/",
        FilteredCostListView.as_view(),
        name="cost_centre_filter",
    ),
    path(
        "costcentrehistoricalfilter/<year>/",
        HistoricalFilteredCostListView.as_view(),
        name="historical_cost_centre_filter",
    ),
]
