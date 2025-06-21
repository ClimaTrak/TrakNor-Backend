from rest_framework import serializers

from .models import WorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = [
            "id",
            "code",
            "equipment",
            "status",
            "revision",
            "priority",
            "scheduled_date",
            "completed_date",
            "created_by",
            "description",
            "cost",
        ]
        read_only_fields = ["id", "code", "status", "completed_date"]


class WorkOrderStatusSerializer(serializers.ModelSerializer):
    """Serializer used for status updates only."""

    class Meta:
        model = WorkOrder
        fields = ["status", "revision"]


class WorkOrderSerializerList(serializers.Serializer):
    """Serializer for work order listings."""

    id = serializers.IntegerField()
    number = serializers.CharField(source="code")
    status = serializers.CharField()
    description = serializers.CharField()
    assignee = serializers.IntegerField(source="created_by_id")


class WorkOrderSerializerOpen(WorkOrderSerializerList):
    """Serializer for open work order listings."""

    pass
