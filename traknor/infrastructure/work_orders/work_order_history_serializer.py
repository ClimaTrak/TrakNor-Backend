from rest_framework import serializers

from traknor.infrastructure.models.work_order_history import WorkOrderHistory


class WorkOrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderHistory
        fields = [
            "id",
            "work_order",
            "old_status",
            "new_status",
            "changed_by",
            "changed_at",
        ]
        read_only_fields = fields
