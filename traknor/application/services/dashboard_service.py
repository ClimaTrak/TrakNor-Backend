from datetime import date, timedelta

from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.work_orders.models import WorkOrder


def get_dashboard_summary() -> dict:
    today = date.today()
    last_30 = today - timedelta(days=30)

    total_equipment = EquipmentModel.objects.count()
    open_work_orders = WorkOrder.objects.exclude(status="Concluída").count()
    work_orders_last_30_days = WorkOrder.objects.filter(
        scheduled_date__gte=last_30
    ).count()
    critical_equipment = EquipmentModel.objects.filter(criticality="Alta").count()

    return {
        "total_equipment": total_equipment,
        "open_work_orders": open_work_orders,
        "work_orders_last_30_days": work_orders_last_30_days,
        "critical_equipment": critical_equipment,
    }
