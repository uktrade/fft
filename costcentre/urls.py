from django.urls import path

from .views import FilteredCostHistoricalListView, FilteredCostListView

urlpatterns = [
    path(
        "costcentrefilter/",
        FilteredCostListView.as_view(),
        name="cost_centre_filter",
    ),
    path(
        "costcentrehistoricalfilter/",
        FilteredCostHistoricalListView.as_view(),
        name="historical_cost_centre_filter",
    ),
]
