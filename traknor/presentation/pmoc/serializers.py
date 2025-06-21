from rest_framework import serializers


class PmocPdfSerializer(serializers.Serializer):
    schedule = serializers.ListField(child=serializers.CharField())
