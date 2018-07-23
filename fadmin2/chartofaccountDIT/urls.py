from django.urls import path, re_path
from . import views

urlpatterns = [
    path('naturalcode/', views.naturalcode, name='naturalcode')
]

