from django.urls import path
from . import views

urlpatterns = [
    path('costcentrefilter/', views.FilteredCostListView.as_view(), name='costcentrefilter'),
]
