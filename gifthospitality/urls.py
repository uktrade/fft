from django.urls import path
from .views import FilteredGiftHospitalityView, GiftHospitalityCreate, \
    GiftHospitalityDelete, GiftHospitalityUpdate, gifthospitalitycreate

urlpatterns = [
    path('add/', GiftHospitalityCreate.as_view(), name='gift-add'),
    path('add1/', gifthospitalitycreate, name='gift-add1'),
    path('search/', FilteredGiftHospitalityView.as_view(), name='gift-search'),
    path('<int:pk>/', GiftHospitalityUpdate.as_view(), name='gift-update'),
    path('<int:pk>/delete/', GiftHospitalityDelete.as_view(), name='gift-delete'),
]