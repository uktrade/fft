from django.urls import path

from .views import FilteredAnalysis2ListView, FilteredCommercialCategoryListView, \
    FilteredExpenditureCategoryListView, FilteredNACListView, FilteredProgrammeView

urlpatterns = [
    path('naturalcode/', FilteredNACListView.as_view(), name='naturalcode'),
    path('financecategory/', FilteredExpenditureCategoryListView.as_view(),
         name='financecategory'),
    path('commercialcategory/', FilteredCommercialCategoryListView.as_view(),
         name='commercialcategory'),
    path('analysis2/', FilteredAnalysis2ListView.as_view(), name='analysis2'),
    path('programmefilter/', FilteredProgrammeView.as_view(), name='programmefilter'),

]
