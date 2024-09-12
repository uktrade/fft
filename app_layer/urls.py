from django.urls import path
from app_layer.views import sns_notification

urlpatterns = [
    # SNS notification endpoint
    path('sns-notification/', sns_notification, name='sns_notification'),
]