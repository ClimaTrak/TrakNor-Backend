from rest_framework import serializers

from .models import AssetModel


class AssetSerializer(serializers.Serializer):
    """Representation serializer used for responses."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    tag = serializers.CharField()
    model = serializers.IntegerField(source="model_id")
    location = serializers.JSONField()
    created_at = serializers.DateTimeField()


class AssetCreateSerializer(serializers.ModelSerializer):
    """Serializer for asset creation."""

    class Meta:
        model = AssetModel
        fields = ["id", "name", "tag", "model", "location", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"tag": {"validators": []}}


class AssetUpdateSerializer(serializers.ModelSerializer):
    """Serializer for asset updates."""

    class Meta:
        model = AssetModel
        fields = ["name", "tag", "model", "location"]
        extra_kwargs = {"tag": {"validators": []}}
