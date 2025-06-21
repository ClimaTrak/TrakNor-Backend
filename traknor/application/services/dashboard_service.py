from datetime import date, timedelta

from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.work_orders.models import WorkOrder


def get_kpis() -> dict:
    done_qs = WorkOrder.objects.filter(
        status="Concluída", completed_date__isnull=False, scheduled_date__isnull=False
    )
    open_orders = WorkOrder.objects.exclude(status="Concluída").count()
    if done_qs.exists():
        total_duration = sum(
            (wo.completed_date - wo.scheduled_date).days for wo in done_qs
        )
        mttr = total_duration / done_qs.count()
    else:
        mttr = 0
    mtbf = 0
    total_orders = WorkOrder.objects.count()
    preventive_ratio = done_qs.count() / total_orders if total_orders else 0
    return {
        "mttr": mttr,
        "mtbf": mtbf,
        "openOrders": open_orders,
        "preventiveRatio": preventive_ratio,
    }


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
