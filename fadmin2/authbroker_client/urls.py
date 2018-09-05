from django.urls import path

from .views import AuthView, AuthCallbackView

urlpatterns = [
    path('login/', AuthView.as_view(), name='authbroker_login'),
    path('callback/', AuthCallbackView.as_view(), name='authbroker_callback'),
]
