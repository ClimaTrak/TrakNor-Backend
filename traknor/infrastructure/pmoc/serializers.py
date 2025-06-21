from rest_framework import serializers


class GeneratePmocSerializer(serializers.Serializer):
    assetId = serializers.UUIDField()
    frequency = serializers.ChoiceField(
        choices=["monthly", "bimonthly", "quarterly", "semester", "yearly"]
    )
    startDate = serializers.DateField(required=False)
