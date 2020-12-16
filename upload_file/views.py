from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.urls import reverse

from upload_file.models import FileUpload
from upload_file.utils import user_has_upload_permission


class UploadedView(UserPassesTestMixin, TemplateView):
    template_name = "upload_file/uploaded_files.html"

    def test_func(self):
        return user_has_upload_permission(self.request.user)

    def handle_no_permission(self):
        return redirect(reverse("index",))

    def uploaded_files(self):
        uploaded_files = FileUpload.objects.filter(
            Q(document_type=FileUpload.ACTUALS) | Q(document_type=FileUpload.BUDGET)
        ).order_by("-created")

        return uploaded_files
