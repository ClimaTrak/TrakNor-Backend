from rest_framework import serializers

from .models import EquipmentModel


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = [
            'id',
            'name',
            'description',
            'type',
            'location',
            'criticality',
            'status',
        ]
