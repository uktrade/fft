from django.urls import path

from .views import FilteredAnalysis1ListView, FilteredAnalysis2ListView, \
    FilteredCommercialCategoryListView, \
    FilteredExpenditureCategoryListView, FilteredFCOMappingView, FilteredInterEntityView, \
    FilteredNACListView, FilteredProgrammeView, FilteredProjectView, \
    HistoricalFilteredProgrammeView, HistoricalFilteredNACListView, \
    HistoricalFilteredExpenditureCategoryListView, HistoricalFilteredCommercialCategoryListView, \
    HistoricalFilteredAnalysis1ListView, HistoricalFilteredAnalysis2ListView

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
    path('projectfilter/', FilteredProjectView.as_view(), name='projectfilter'),
    path('fcofilter/', FilteredFCOMappingView.as_view(), name='fcofilter'),
    # Historical data
    path('historicalnaturalcode/', HistoricalFilteredNACListView.as_view(), name='historicalnaturalcode'),
    path('historicalfinancecategory/', HistoricalFilteredExpenditureCategoryListView.as_view(),
         name='historicalfinancecategory'),
    path('historicalcommercialcategory/', HistoricalFilteredCommercialCategoryListView.as_view(),
         name='historicalcommercialcategory'),
    path('historicalanalysis1/', HistoricalFilteredAnalysis1ListView.as_view(), name='historicalanalysis1'),
    path('historicalanalysis2/', HistoricalFilteredAnalysis2ListView.as_view(), name='historicalanalysis2'),
    path('historicalprogrammefilter/', HistoricalFilteredProgrammeView.as_view(), name='historicalprogrammefilter'),
    path('historicalinterentityfilter/', FilteredInterEntityView.as_view(), name='historicalinterentityfilter'),
    path('historicalprojectfilter/', FilteredProjectView.as_view(), name='historicalprojectfilter'),
    path('historicalfcofilter/', FilteredFCOMappingView.as_view(), name='historicalfcofilter'),

]
