from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('costcentres/', views.CostcentreListView.as_view(), name='costcentres'),
    path('directorates/', views.DirectorateListView.as_view(), name='directorates'),
    path('groups/', views.DepartmentalGroupListView.as_view(), name='groups'),
]
