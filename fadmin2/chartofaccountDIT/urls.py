from django.urls import path, re_path
from . import views


urlpatterns = [
    path('naturalcode/', views.FilteredNACListView.as_view(), name='naturalcode'),
    path('financecategory/', views.FilteredExpenditureCategoryListView.as_view(), name='financecategory'),
    path('commercialcategory/', views.FilteredCommercialCategoryListView.as_view(), name='commercialcategory'),
    path('analysis2/', views.FilteredAnalysis2ListView.as_view(), name='analysis2')
]

