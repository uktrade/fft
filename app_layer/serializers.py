# app_layer/serializers.py
from rest_framework import serializers


class S3EventSerializer(serializers.Serializer):
    bucket = serializers.CharField()
    key = serializers.CharField()