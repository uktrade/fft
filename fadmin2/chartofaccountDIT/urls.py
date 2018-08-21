from django.urls import path, re_path
from . import views


urlpatterns = [
    path('naturalcode/', views.FilteredNACListView.as_view(), name='naturalcode'),
    path('financecategory/', views.FilteredExpenditureCategoryListView.as_view(), name='financecategory')
]

