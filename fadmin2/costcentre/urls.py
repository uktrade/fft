from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('costcentres/', views.CostcentreListView.as_view(), name='costcentres'),
]
