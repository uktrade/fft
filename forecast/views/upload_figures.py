from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from forecast.forms import (
    UploadActualsForm,
)
from forecast.import_actuals import (
    upload_trial_balance_report,
)
from forecast.tasks import process_uploaded_file

from upload_file.decorators import has_upload_permission
from upload_file.models import FileUpload


class UploadActualsView(FormView):
    template_name = "forecast/file_upload.html"
    form_class = UploadActualsForm
    success_url = reverse_lazy("uploaded_files")

    @has_upload_permission
    def dispatch(self, *args, **kwargs):
        return super(UploadActualsView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            data = form.cleaned_data

            file_upload = FileUpload(
                document_file=request.FILES['file'],
                uploading_user=request.user,
            )
            file_upload.save()
            # Process file async

            if settings.ASYNC_FILE_UPLOAD:
                process_uploaded_file.delay(
                    upload_trial_balance_report,
                    data['period'].period_calendar_code,
                    data['year'].financial_year,
                )
            else:
                process_uploaded_file(
                    upload_trial_balance_report,
                    data['period'].period_calendar_code,
                    data['year'].financial_year,
                )

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
