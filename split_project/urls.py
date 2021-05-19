from django.urls import path

from split_project.views import (
    UploadedPercentageView,
    UploadPercentageView,
    export_split_percentage_data,
    export_split_percentage_template,
)

urlpatterns = [
    path(
        "project_percentage/",
        UploadedPercentageView.as_view(),
        name="project_percentage",
    ),
    path(
        "upload_percentage_file/",
        UploadPercentageView.as_view(),
        name="upload_percentage_file",
    ),
    path(
        "download_template_file/",
        export_split_percentage_template,
        name="download_template_file",
    ),
    path(
        "download_opercentage/",
        export_split_percentage_data,
        name="download_opercentage",
    ),
]
