from django.urls import path

from .views import FilteredCostListView

urlpatterns = [
    path('costcentrefilter/', FilteredCostListView.as_view(), name='costcentrefilter'),
]
