from __future__ import annotations

from datetime import date, timedelta

from traknor.application.services.work_order_service import _to_domain
from traknor.domain.metrics.kpi_calculator import compute
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.work_orders.models import WorkOrder
from traknor.domain.constants import WorkOrderStatus


def get_kpis(
    *,
    range_from: date | None = None,
    range_to: date | None = None,
    equipment_id: int | None = None,
    group_by: str | None = None,
) -> dict:
    """Return KPI metrics for the given filters."""

    if range_from is None:
        range_from = date.today().replace(day=1)
    if range_to is None:
        range_to = date.today()

    closed_qs = WorkOrder.objects.filter(
        status=WorkOrderStatus.DONE.value,
        completed_date__isnull=False,
        completed_date__range=(range_from, range_to),
    )
    if equipment_id:
        closed_qs = closed_qs.filter(equipment_id=equipment_id)

    workorders = [_to_domain(obj) for obj in closed_qs]
    open_count = WorkOrder.objects.exclude(status=WorkOrderStatus.DONE.value).count()
    closed_count = closed_qs.count()

    result = compute(
        workorders,
        range_from,
        range_to,
        group_by=group_by,
        open_count=open_count,
        closed_count=closed_count,
    )

    data = {
        "range": {"from": str(result.range_from), "to": str(result.range_to)},
        "mtbf": result.mtbf,
        "mttr": result.mttr,
        "open_workorders": result.open_workorders,
        "closed_workorders": result.closed_workorders,
    }

    if result.series:
        data["series"] = {
            "labels": result.series.labels,
            "mtbf": result.series.mtbf,
            "mttr": result.series.mttr,
            "closed": result.series.closed,
        }

    return data


def get_dashboard_summary() -> dict:
    today = date.today()
    last_30 = today - timedelta(days=30)

    total_equipment = EquipmentModel.objects.count()
    open_work_orders = WorkOrder.objects.exclude(status=WorkOrderStatus.DONE.value).count()
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
