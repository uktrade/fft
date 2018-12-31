from bootstrap_datepicker_plus import DatePickerInput

from core.filters import MyFilterSet

from django_filters import DateFilter, ModelChoiceFilter, NumberFilter

from payroll.models import Grade


from .models import GiftAndHospitality, GiftAndHospitalityCategory, \
    GiftAndHospitalityClassification, GiftAndHospitalityCompany


class GiftHospitalityFilter(MyFilterSet):
    entered_date_stamp_from = DateFilter(field_name='entered_date_stamp',
                                         label='Date Entered From:',
                                         lookup_expr='gte',
                                         widget=DatePickerInput(
                                             options={
                                                 "format": "DD/MM/YYYY",  # moment date-time format
                                                 "showClose": True,
                                                 "showClear": True,
                                                 "showTodayButton": True,
                                             }))
    entered_date_stamp_to = DateFilter(field_name='entered_date_stamp',
                                       label='To:', lookup_expr='lte',
                                       widget=DatePickerInput(
                                           options={
                                               "format": "DD/MM/YYYY",  # moment date-time format
                                               "showClose": True,
                                               "showClear": True,
                                               "showTodayButton": True,
                                           }))
    value = NumberFilter(lookup_expr='lte', label='Max value of offer (£)')

    # use a dropdown to search the following fields
    company = ModelChoiceFilter(queryset=GiftAndHospitalityCompany.objects.all())

    class Meta(MyFilterSet.Meta):
        model = GiftAndHospitality
        fields = ['id',
                  'category_fk',
                  'classification_fk',
                  'value',
                  'rep',
                  'grade_fk',
                  'offer',
                  'company',
                  'action_taken',
                  'entered_date_stamp_from',
                  'entered_date_stamp_to',
                  ]
