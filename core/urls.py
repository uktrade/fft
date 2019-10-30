from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.AboutView.as_view(), name="about"),
    path("testupload", views.DocumentCreateView.as_view(), name="testupload"),
]
