from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    total_equipment = serializers.IntegerField()
    open_work_orders = serializers.IntegerField()
    work_orders_last_30_days = serializers.IntegerField()
    critical_equipment = serializers.IntegerField()
