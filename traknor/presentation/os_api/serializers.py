from rest_framework import serializers


class ExecuteResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField()
    duration = serializers.IntegerField()
