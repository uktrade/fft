from django.urls import path
from .views import FilteredGiftHospitalityView,  GiftHospitalityView, GiftHospitalityReceivedView

urlpatterns = [
    path('receive/', GiftHospitalityReceivedView.as_view(), name='gift-received'),
    path('offer/', GiftHospitalityView.as_view(), name='gift-offered'),
    path('search/', FilteredGiftHospitalityView.as_view(), name='gift-search'),
]