from django.urls import path

from oscar_return.views import export_oscar_report

urlpatterns = [
    path("download_oscar/", export_oscar_report, name="download_oscar"),
]
