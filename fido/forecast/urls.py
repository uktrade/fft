from django.urls import path

from .views import (
    CostClassView,
    MultiforecastView,
    PivotClassView,
    pivot_test1,
    edit_forecast,
)

urlpatterns = [
    path('pivot/', PivotClassView.as_view(), name='pivot'),
    path('costcentre/', CostClassView.as_view(), name='costcentre'),
    path('pivotmulti/', MultiforecastView.as_view(), name='pivotmulti'),
    path('pivot1/', pivot_test1, name='pivot1'),
    path('edit/', edit_forecast, name='edit')
]