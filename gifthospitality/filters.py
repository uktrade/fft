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

# class GiftHospitalityFilter(MyFilterSet):
#     """Use a single text box to enter an object name.
#     It will search into all available fields
#     """
#     search_all = django_filters.CharFilter(field_name='', label='',
#                                                 method='search_all_filter')
#
#
#     def search_all_filter(self, queryset, name, value):
#         return queryset.filter(Q(id__icontains=value) |
#                                 Q(gift_type__icontains=value) |
#                                 Q(category__icontains=value) |
#                                 Q(classification__icontains=value) |
#                                 Q(group_name__icontains=value) |
#                                 Q(venue__icontains=value) |
#                                 Q(reason__icontains=value) |
#                                 Q(value__icontains=value) |
#                                 Q(band__icontains=value) |
#                                 Q(rep__icontains=value) |
#                                 Q(grade__icontains=value) |
#                                 Q(offer__icontains=value) |
#                                 Q(company_rep__icontains=value) |
#                                 Q(company__icontains=value) |
#                                 Q(action_taken__icontains=value) |
#                                 Q(entered_by__icontains=value)
#                                )
#
#     # entered_date_stamp__range = (start_date, end_date))
#     class Meta(MyFilterSet.Meta):
#         model = GiftAndHospitality
#         fields = [
#             'search_all',
#         ]
