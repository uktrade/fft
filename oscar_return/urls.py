from django.urls import path

from oscar_return.views import export_oscar_report, export_previous_year_oscar_report


urlpatterns = [
    path("download_oscar/", export_oscar_report, name="download_oscar"),
    path(
        "download_previous_year_oscar/",
        export_previous_year_oscar_report,
        name="download_previous_year_oscar",
    ),
]
