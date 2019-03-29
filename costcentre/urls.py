from django.urls import path

from .views import FilteredCostListView, FilteredCostHistoricalListView

urlpatterns = [
    path('costcentrefilter/', FilteredCostListView.as_view(), name='costcentrefilter'),
    path('costcentrehistoricalfilter/', FilteredCostHistoricalListView.as_view(), name='costcentrehistoricalfilter'),

]
