from django.urls import path

from .views import adireport

urlpatterns = [
    path('forecast/', adireport, name='forecast')
]
