from django.db.models import Q
from django.views.generic.base import TemplateView

from upload_file.decorators import has_upload_permission
from upload_file.models import FileUpload


class UploadedView(TemplateView):
    template_name = "upload_file/uploaded_files.html"

    @has_upload_permission
    def dispatch(self, request, *args, **kwargs):
        return super(UploadedView, self).dispatch(request, *args, **kwargs)

    def uploaded_files(self):
        uploaded_files = FileUpload.objects.filter(
            Q(document_type=FileUpload.ACTUALS) | Q(document_type=FileUpload.BUDGET)
        ).order_by("-created")

        return uploaded_files
