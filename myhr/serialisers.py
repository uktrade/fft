from rest_framework import serializers

from myhr.models import Group


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for Group model.
    """
    class Meta:
        model = Group
        fields = [
            "group",
            "fte",
            "count"
        ]
        read_only_fields = fields