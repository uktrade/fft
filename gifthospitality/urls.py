from django.urls import path
from .views import FilteredGiftHospitalityView,  GiftHospitalityOfferedView, \
    GiftHospitalityReceivedView, GiftHospitalityDoneView

app_name = 'gifthospitality'
urlpatterns = [
    path('receive/', GiftHospitalityReceivedView.as_view(), name='gift-received'),
    path('offer/', GiftHospitalityOfferedView.as_view(), name='gift-offered'),
    path('search/', FilteredGiftHospitalityView.as_view(), name='gift-search'),
    path('done/', GiftHospitalityDoneView.as_view(), name='gifthospitality_done'),
]