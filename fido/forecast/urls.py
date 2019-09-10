from django.urls import path

from .views import MultiforecastView, PivotClassView, pivot_test1

urlpatterns = [
    path('pivot/', PivotClassView.as_view(), name='pivot'),
    path('pivotmulti/', MultiforecastView.as_view(), name='pivotmulti'),
    path('pivot1/', pivot_test1, name='pivot1')
]