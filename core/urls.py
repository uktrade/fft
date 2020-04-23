from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout, name="logout"),
    path("testupload", views.DocumentCreateView.as_view(), name="testupload"),
]
