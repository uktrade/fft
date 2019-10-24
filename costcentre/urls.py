from django.urls import path

from .views import FilteredCostHistoricalListView, FilteredCostListView

urlpatterns = [
    path("costcentrefilter/", FilteredCostListView.as_view(), name="costcentrefilter"),
    path(
        "costcentrehistoricalfilter/",
        FilteredCostHistoricalListView.as_view(),
        name="costcentrehistoricalfilter",
    ),
]
