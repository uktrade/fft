from django.urls import reverse_lazy

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormView

from forecast.utils.access_helpers import (
    can_download_mi_reports,
    can_download_oscar,
)

from future_years.forms import DownloadFutureForm

class DownloadViewBase(UserPassesTestMixin, FormView):
    template_name = "forecast/file_upload.html"
    form_class = DownloadFutureForm

    def test_func(self):
        return can_download_mi_reports(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section_name"] = self.context
        return context

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)

    def get_success_url(self):
        success_url = reverse_lazy(
            self.success_name, kwargs={"financial_year": self.financial_year}
        )
        return success_url

    def form_valid(self, form):
        self.financial_year = form.cleaned_data["download_year"]
        return super().form_valid(form)

        # if form.is_valid():
        #     data = form.cleaned_data
        #
        #     # When using a model form, you must use the
        #     # name attribute of the file rather than
        #     # passing the request file var directly as this is the
        #     # required when using the chunk uploader project
        #     s3_file_name = request.FILES['file'].name
        #
        #     logger.info(f"s3_file_name is f{s3_file_name}")
        #
        #     file_upload = FileUpload(
        #         s3_document_file=s3_file_name,
        #         uploading_user=request.user,
        #         document_type=self.upload_type,
        #     )
        #     file_upload.save()
        #
        #     logger.info("Saved file to S3")
        #
        #     # Process file async
        #     args = self.get_args(data)
        #     if settings.ASYNC_FILE_UPLOAD:
        #         logger.info("Using worker to upload file")
        #         process_uploaded_file.delay(*args)
        #     else:
        #         process_uploaded_file(*args)
        #
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)


class DownloadForecastView(DownloadViewBase):
    success_name = "download_mi_report_source"
    context = "Download Future Forecast"

    def get_args(self, data):
        return [
                data['year'].financial_year,
                ]
