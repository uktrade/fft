from django.urls import path

from .views import FilteredAnalysis1ListView, FilteredAnalysis2ListView, \
    FilteredCommercialCategoryListView, \
    FilteredExpenditureCategoryListView, FilteredInterEntityView, \
    FilteredNACListView, FilteredProgrammeView

urlpatterns = [
    path('naturalcode/', FilteredNACListView.as_view(), name='naturalcode'),
    path('financecategory/', FilteredExpenditureCategoryListView.as_view(),
         name='financecategory'),
    path('commercialcategory/', FilteredCommercialCategoryListView.as_view(),
         name='commercialcategory'),
    path('analysis1/', FilteredAnalysis1ListView.as_view(), name='analysis1'),
    path('analysis2/', FilteredAnalysis2ListView.as_view(), name='analysis2'),
    path('programmefilter/', FilteredProgrammeView.as_view(), name='programmefilter'),
    path('interentityfilter/', FilteredInterEntityView.as_view(), name='interentityfilter'),

]
