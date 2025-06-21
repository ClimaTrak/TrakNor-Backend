from rest_framework import serializers


class EquipmentImportSerializer(serializers.Serializer):
    file = serializers.FileField()


class ImportResultSerializer(serializers.Serializer):
    created = serializers.IntegerField()
    errors = serializers.ListField()
