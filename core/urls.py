from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout, name="logout"),
    path("accessibility", views.AccessibilityPageView.as_view(), name="accessibility"),
]
