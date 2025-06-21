from rest_framework import serializers


class ReportResponseSerializer(serializers.Serializer):
    data = serializers.CharField()
