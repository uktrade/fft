from bootstrap_datepicker_plus import DatePickerInput

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
from django.views.generic.edit import FormView

class GiftHospitalityView(FormView):
    template_name = 'gifthospitality/giftandhospitality_form.html'
    form_class = GiftAndHospitalityForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.instance.entered_by = self.request.user.first_name + ' ' + self.request.user.last_name
        form.instance.company = form.instance.company_fk
        form.instance.category = form.instance.category_fk
        form.instance.classification = form.instance.classification_fk
        obj = form.save(commit=False)
        obj.type = obj.classification_fk.gift_type
        if obj.rep_fk:
            obj.rep = obj.rep_fk
            obj.staff_no = obj.rep_fk.employee_number
            obj.grade = obj.rep_fk.grade
            obj.grade = obj.rep_fk.cost_centre.directorate.group.group_name
        obj.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


# def gifthospitalitycreate(request):
#     form = GiftAndHospitalityForm()
#
#     if request.method == "POST":
#         form = GiftAndHospitalityForm(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
#             return gifthospitalitycreate(request)
#         else:
#             print('ERROR FORM INVALID')
#
#     return render(request,'gifthospitality/giftandhospitality_form.html',{'form':form})





class GiftHospitalityCreate(CreateView):
    model = GiftAndHospitality

    def get_form(self):
        form = super().get_form()
        form.fields['date_offered'].widget = DatePickerInput(
            options={
                "format": "DD/MM/YYYY",  # moment date-time format
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            }
        )
        return form
    # fields = ['classification','group_name', 'date_offered', 'venue', 'reason']
    fields = [
        'classification_fk',
        'group_name',
        'date_offered',
        'venue',
        'reason',
        'value',
        'rep',
        'offer',
        'company_rep',
        'company_fk',
        'action_taken',
        'entered_by',
        'staff_no',
        # 'entered_date_stamp',
        'category_fk',
        # 'category',
        'grade'
    ]


class GiftHospitalityUpdate(UpdateView):
    model = GiftAndHospitality
    fields = ['classification']

class GiftHospitalityDelete(DeleteView):
    model = GiftAndHospitality
    success_url = reverse_lazy('author-list')