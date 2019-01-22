# gifthospitality/views.py
from json import dumps

from core.utils import today_string
from core.views import FAdminFilteredView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .filters import GiftHospitalityFilter
from .forms import GiftAndHospitalityOfferedForm, GiftAndHospitalityReceivedForm
from .models import GiftAndHospitalityClassification
from .tables import GiftHospitalityTable


class FilteredGiftHospitalityView(LoginRequiredMixin, FAdminFilteredView):
    table_class = GiftHospitalityTable
    model = table_class.Meta.model
    filterset_class = GiftHospitalityFilter
    template_name = 'gifthospitality/gifthospitality_filter.html'
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
        context['section_description'] = 'If you have accepted or declined any gift or hospitality ' \
                                         'over £10 you must record it in the Register below.  ' \
                                         'The DIT Gifts & Hospitality Policy is '
        qs = GiftAndHospitalityClassification.objects.values('pk', 'gift_type')
        list_vals = []
        for item in qs:
            list_vals.append([str(item['pk']), item['gift_type']])
        l1 = dumps(list_vals)
        context['gift_type'] = l1
        return context


class GiftHospitalityOfferedView(GiftHospitalityReceivedView):
    form_class = GiftAndHospitalityOfferedForm
    success_name = 'gifthospitality:offered-done'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Add Gift/Hospitality Offered'
        context['section_description'] = 'If you have offered gifts or hospitality ' \
                                         'you must record it in the Register below.  ' \
                                         'The DIT Gifts & Hospitality Policy is '
        context['gift_type'] = '[]'
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
