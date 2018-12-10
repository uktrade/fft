#gifthospitality/views.py

from core.utils import today_string

from core.views import FAdminFilteredView

from django.urls import reverse_lazy
from django.urls import path
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import GiftHospitalityFilter
from .tables import GiftHospitalityTable

from .forms import GiftAndHospitalityReceivedForm, \
    GiftAndHospitalityOfferedForm
from django.views.generic.edit import FormView

from django.views.generic.base import TemplateView

class FilteredGiftHospitalityView(LoginRequiredMixin, FAdminFilteredView):
    table_class = GiftHospitalityTable
    model = table_class.Meta.model
    filterset_class = GiftHospitalityFilter
    export_name = 'Gifts and Hospitality' + today_string()
    sheet_name = 'Gifts and Hospitality'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Search Gifts and Hospitality Records'
        return context


class GiftHospitalityReceivedView(FormView):
    template_name = 'gifthospitality/giftandhospitality_form.html'
    form_class = GiftAndHospitalityReceivedForm
    success_name = 'gifthospitality:received-done'
    def get_success_url(self):
        success_url = reverse_lazy(self.success_name, kwargs={'gift_id': self.new_id})
        return success_url

    def form_valid(self, form):
        form.instance.entered_by = self.request.user.first_name + ' ' + self.request.user.last_name
        obj = form.save()
        self.new_id = obj.pk
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Add Gift/Hospitality Received'
        return context


class GiftHospitalityOfferedView(GiftHospitalityReceivedView):
    form_class = GiftAndHospitalityOfferedForm
    success_name = 'gifthospitality:offered-done'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Add Gift/Hospitality Offered'
        return context



class GiftHospitalityOfferedDoneView(TemplateView):
    template_name = 'gifthospitality/giftandhospitality_added.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Completed Gift/Hospitality Offered'
        return context


class GiftHospitalityReceivedDoneView(TemplateView):
    template_name = 'gifthospitality/giftandhospitality_added.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Completed Gift/Hospitality Received'
        return context



