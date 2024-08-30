from django.urls import path
from app_layer.views import s3_event, add_transaction

urlpatterns = [
    path('api/s3-event/', s3_event, name='s3_event'),
    path('api/transactions/', add_transaction, name='add_transaction'),
]