from django.urls import path

from future_years.views import DownloadForecastView

urlpatterns = [
    path(
        "download_future_forecast",
        DownloadForecastView.as_view(),
        name="download_future_forecast",
    ),
]
