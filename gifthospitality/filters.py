from  django_filters import DateFromToRangeFilter, NumberFilter, CharFilter, ModelChoiceFilter

from .models import GiftAndHospitality, GiftAndHospitalityCategory, \
    GiftAndHospitalityClassification, GiftAndHospitalityCompany

from core.filters import MyFilterSet
from payroll.models import Grade

class GiftHospitalityFilter(MyFilterSet):
    entered_date_stamp = DateFromToRangeFilter()
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
            'entered_date_stamp',
        ]

