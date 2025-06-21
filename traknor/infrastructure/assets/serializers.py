from rest_framework import serializers

from .models import AssetModel


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetModel
        fields = [
            "id",
            "name",
            "tag",
            "model",
            "location",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"tag": {"validators": []}}
