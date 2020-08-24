import logging

from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from forecast.forms import (
    UploadActualsForm,
    UploadBudgetsForm,
)
from forecast.tasks import process_uploaded_file

from upload_file.decorators import has_upload_permission
from upload_file.models import FileUpload


logger = logging.getLogger(__name__)


class UploadActualsView(FormView):
    template_name = "forecast/file_upload.html"
    form_class = UploadActualsForm
    success_url = reverse_lazy("uploaded_files")

    @has_upload_permission
    def dispatch(self, *args, **kwargs):
        return super(UploadActualsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section_name"] = "Upload Actuals"
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
                document_file=s3_file_name,
                uploading_user=request.user,
                document_type=FileUpload.ACTUALS,
            )
            file_upload.save()

            logger.info("Saved file to S3")

            # Process file async
            if settings.ASYNC_FILE_UPLOAD:
                logger.info("Using worker to upload file")
                process_uploaded_file.delay(
                    data['period'].period_calendar_code,
                    data['year'].financial_year,
                )
            else:
                process_uploaded_file(
                    data['period'].period_calendar_code,
                    data['year'].financial_year,
                )

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UploadBudgetView(FormView):
    template_name = "forecast/file_upload.html"
    form_class = UploadBudgetsForm
    success_url = reverse_lazy("uploaded_files")

    @has_upload_permission
    def dispatch(self, *args, **kwargs):
        return super(UploadBudgetView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section_name"] = "Upload Budgets"
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            data = form.cleaned_data

            # When using a model form, you must use the
            # name attribute of the file rather than
            # passing the request file var directly as this is the
            # required when using the chunk uploader project
            s3_file_name = request.FILES['file'].name

            file_upload = FileUpload(
                document_file=s3_file_name,
                uploading_user=request.user,
                document_type=FileUpload.BUDGET,
            )
            file_upload.save()
            # Process file async

            if settings.ASYNC_FILE_UPLOAD:
                process_uploaded_file.delay(
                    data['year'].financial_year,
                )
            else:
                process_uploaded_file(
                    data['year'].financial_year,
                )

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
