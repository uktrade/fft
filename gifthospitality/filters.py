from  django_filters import DateFromToRangeFilter, NumberFilter, CharFilter, ModelChoiceFilter, \
    DateFilter
from django_filters.widgets import SuffixedMultiWidget

from .models import GiftAndHospitality, GiftAndHospitalityCategory, \
    GiftAndHospitalityClassification, GiftAndHospitalityCompany

from core.filters import MyFilterSet
from payroll.models import Grade

from bootstrap_datepicker_plus import DatePickerInput


class GiftHospitalityFilter(MyFilterSet):
    entered_date_stamp_from = DateFilter(field_name = 'entered_date_stamp',
                                         label='Date Entered From:',
                                            lookup_expr='gte',
                                         widget=DatePickerInput(
                    options={
                        "format": "DD/MM/YYYY",  # moment date-time format
                        "showClose": True,
                        "showClear": True,
                        "showTodayButton": True,
                    }))
    entered_date_stamp_to = DateFilter(field_name = 'entered_date_stamp',
                                       label = 'To:', lookup_expr='lte',
                                         widget=DatePickerInput(
                    options={
                        "format": "DD/MM/YYYY",  # moment date-time format
                        "showClose": True,
                        "showClear": True,
                        "showTodayButton": True,
                    }))
    value = NumberFilter(lookup_expr='lte', label='Max value of offer (£)' )

    # use a dropdown to search the following fields
    category =  ModelChoiceFilter(queryset=GiftAndHospitalityCategory.objects.all())
    gift_type =  ModelChoiceFilter(queryset=GiftAndHospitalityClassification.objects.all())
    company =  ModelChoiceFilter(queryset=GiftAndHospitalityCompany.objects.all())
    grade = ModelChoiceFilter(queryset=Grade.objects.all())

    class Meta(MyFilterSet.Meta):
            model = GiftAndHospitality
            fields = [ 'id',
            'category',
            'gift_type',
            'value',
            'rep',
            'grade',
            'offer',
            'company',
            'action_taken',
            'entered_date_stamp_from',
            'entered_date_stamp_to',
            ]
