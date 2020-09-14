from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.forms import EndOfMonthProcessForm
from end_of_month.utils import (
    InvalidPeriodError,
    PeriodAlreadyArchivedError,
    get_archivable_month,
    user_has_archive_access,
)

from forecast.models import FinancialPeriod
from forecast.utils.access_helpers import is_system_locked


class EndOfMonthProcessView(
    UserPassesTestMixin, FormView,
):
    template_name = "end_of_month/end_of_month_archive.html"
    form_class = EndOfMonthProcessForm
    period_code = None
    success_name = "forecast_dit"

    def get_success_url(self):
        success_url = reverse_lazy(
            self.success_name, kwargs={"period": self.period_code}
        )
        return success_url

    def test_func(self):
        can_edit = user_has_archive_access(
            self.request.user
        )

        if not can_edit:
            raise PermissionDenied()

        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locked"] = is_system_locked()
        try:
            archivable_period = get_archivable_month()
            context["archivable_month"] = FinancialPeriod.objects.get(
                pk=archivable_period).period_long_name
        except InvalidPeriodError:
            context["invalid_period"] = True
        except PeriodAlreadyArchivedError as ex:
            context["already_archived"] = ex
        return context

    def form_valid(self, form):
        archivable_period = get_archivable_month()
        end_of_month_archive(archivable_period)
        self.period_code = archivable_period
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
