from django.urls import path

from .views import (
    ForecastViewSet,
)

urlpatterns = [
    path(
        "forecast/",
        ForecastViewSet.as_view({'get': 'list'}),
        name="data_lake_forecast",
    ),
]
