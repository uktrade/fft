from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import GiftAndHospitality, GiftAndHospitalityCompany, \
    GiftAndHospitalityClassification, GiftAndHospitalityCategory

from core.utils import today_string

from core.views import FAdminFilteredView

from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import GiftHospitalityFilter
from .tables import GiftHospitalityTable


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




from django.shortcuts import render
from .forms import GiftAndHospitalityForm

def gifthospitalitycreate(request):
    form = GiftAndHospitalityForm()

    if request.method == "POST":
        form = GiftAndHospitalityForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return gifthospitalitycreate(request)
        else:
            print('ERROR FORM INVALID')

    return render(request,'gifthospitality/giftandhospitality_form.html',{'form':form})



class GiftHospitalityCreate(CreateView):
    model = GiftAndHospitality
    fields = ['classification','group_name', 'date_offered', 'venue', 'reason']

class GiftHospitalityUpdate(UpdateView):
    model = GiftAndHospitality
    fields = ['classification']

class GiftHospitalityDelete(DeleteView):
    model = GiftAndHospitality
    success_url = reverse_lazy('author-list')