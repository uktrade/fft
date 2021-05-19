import logging

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from forecast.forms import (
    UploadActualsForm,
    UploadBudgetsForm,
)
from forecast.tasks import process_uploaded_file

from upload_file.models import FileUpload
from upload_file.utils import user_has_upload_permission

logger = logging.getLogger(__name__)


class UploadViewBase(UserPassesTestMixin, FormView):
    template_name = "forecast/file_upload.html"

    # form_class = UploadActualsForm
    # success_url = reverse_lazy("uploaded_files")
    # context = "Upload Actuals"
    def test_func(self):
        return user_has_upload_permission(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section_name"] = self.context
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        logger.info("Received file upload attempt")

        if form.is_valid():
            logger.info("File upload form is valid")
            data = form.cleaned_data

            # When using a model form, you must use the
            # name attribute of the file rather than
            # passing the request file var directly as this is the
            # required when using the chunk uploader project
            s3_file_name = request.FILES['file'].name

            logger.info(f"s3_file_name is f{s3_file_name}")

            file_upload = FileUpload(
                s3_document_file=s3_file_name,
                uploading_user=request.user,
                document_type=self.upload_type,
            )
            file_upload.save()

            logger.info("Saved file to S3")

            # Process file async
            if settings.ASYNC_FILE_UPLOAD:
                logger.info("Using worker to upload file")
                args = self.get_args(data)
                process_uploaded_file.delay(*args)
            else:
                process_uploaded_file(*args)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UploadActualsView(UploadViewBase):
    form_class = UploadActualsForm
    success_url = reverse_lazy("uploaded_files")
    context = "Upload Actuals"
    upload_type = FileUpload.ACTUALS

    def get_args(data):
        return [data['period'].period_calendar_code,
                data['year'].financial_year,
                ]


class UploadBudgetView(UploadViewBase):
    form_class = UploadBudgetsForm
    success_url = reverse_lazy("uploaded_files")

    context = "Upload Budgets"
    upload_type = FileUpload.BUDGET

    def get_args(data):
        return [data['year'].financial_year, ]
