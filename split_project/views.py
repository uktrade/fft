import logging
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic.base import TemplateView

from django.urls import reverse, reverse_lazy

from forecast.views.upload_file import UploadViewBase

from split_project.downloads import (
    create_percentage_download,
    create_template,
)

from split_project.forms import UploadPercentageForm
from split_project.templatetags.upload_percentage_permissions import (
    has_project_percentage_permission,
)

from upload_file.models import FileUpload

logger = logging.getLogger(__name__)


class UploadPercentageView(UploadViewBase):
    template_name = "percentage_file_upload.html"
    form_class = UploadPercentageForm
    success_url = reverse_lazy("project_percentage")

    context = "Upload Percentages"
    upload_type = FileUpload.PROJECT_PERCENTAGE

    def get_args(self, data):
        return []

    def test_func(self):
        return has_project_percentage_permission(self.request.user)


class UploadedPercentageView(UserPassesTestMixin, TemplateView):
    template_name = "split_projects.html"

    def test_func(self):
        return has_project_percentage_permission(self.request.user)

    def handle_no_permission(self):
        return redirect(reverse("index",))

    def uploaded_files(self):
        uploaded_files = FileUpload.objects.filter(
            Q(document_type=FileUpload.PROJECT_PERCENTAGE)
        ).order_by("-created")[:1]

        return uploaded_files


@user_passes_test(has_project_percentage_permission, login_url="index")
def export_split_percentage_data(request):
    return create_percentage_download()


@user_passes_test(has_project_percentage_permission, login_url="index")
def export_split_percentage_template(request):
    return create_template()
