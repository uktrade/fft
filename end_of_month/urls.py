from django.urls import path

from end_of_month.views.end_of_month_archive import EndOfMonthProcessView

urlpatterns = [
    path(
        "archive_forecast/",
        EndOfMonthProcessView.as_view(),
        name="end_of_month"
    ),
]
