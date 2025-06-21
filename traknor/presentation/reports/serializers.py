from rest_framework import serializers  # pragma: no cover


class ReportResponseSerializer(
    serializers.Serializer
):  # pragma: no cover - simple container
    data = serializers.CharField()
