from django.urls import path, re_path
from . import views


urlpatterns = [
    path('forecast/', views.adireport, name='forecast')
]
