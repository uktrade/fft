from django.urls import path
from . import views
from .costcentre import CostCentreView
from .directorate import DirectorateView
from .group import GroupView

urlpatterns = [
    path('list/', GroupView.as_view(), name='myhr_list'),
    path('directorate/', DirectorateView.as_view(), name='directorate_view'),
    path('costcentre/', CostCentreView.as_view(), name='costcentre_view'),
]