from __future__ import annotations

from datetime import date
from typing import List
from uuid import uuid4

from traknor.domain.work_order import WorkOrder, WorkOrderHistory
from traknor.domain.constants import WorkOrderStatus
from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.models.work_order_history import (
    WorkOrderHistory as WorkOrderHistoryModel,
)
from traknor.infrastructure.notifications.email import send_work_order_completed
from traknor.infrastructure.work_orders.models import WorkOrder as WorkOrderModel


def _to_domain(obj: WorkOrderModel) -> WorkOrder:
    return WorkOrder(
        id=obj.id,
        code=obj.code,
        equipment_id=obj.equipment_id,
        status=obj.status,
        priority=obj.priority,
        scheduled_date=obj.scheduled_date,
        completed_date=obj.completed_date,
        created_by_id=obj.created_by_id,
        description=obj.description,
        cost=float(obj.cost),
        revision=obj.revision,
        deleted_at=obj.deleted_at,
    )


def _history_to_domain(obj: WorkOrderHistoryModel) -> WorkOrderHistory:
    return WorkOrderHistory(
        id=obj.id,
        work_order_id=obj.work_order_id,
        old_status=obj.old_status,
        new_status=obj.new_status,
        changed_by_id=obj.changed_by_id,
        changed_at=obj.changed_at,
    )


def create(data: dict) -> WorkOrder:
    obj = WorkOrderModel.objects.create(
        code=uuid4(),
        status=WorkOrderStatus.OPEN.value,
        **data,
    )
    return _to_domain(obj)


def update_status(work_order_id: int, new_status: str, changed_by: User) -> WorkOrder:
    obj = WorkOrderModel.objects.get(id=work_order_id)
    valid = {
        "Aberta": ["Em Execução", "Em Espera"],
        "Em Espera": ["Em Execução"],
        "Em Execução": ["Concluída"],
    }
    if new_status not in valid.get(obj.status, []):
        raise ValueError("Invalid status transition")
    WorkOrderHistoryModel.objects.create(
        work_order=obj,
        old_status=obj.status,
        new_status=new_status,
        changed_by=changed_by,
    )
    obj.status = new_status
    if new_status == "Concluída" and obj.completed_date is None:
        obj.completed_date = date.today()
        send_work_order_completed(obj)
    obj.save()
    return _to_domain(obj)


def list_by_filter(
    *,
    status: str | None = None,
    equipment_location: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> List[WorkOrder]:
    qs = WorkOrderModel.objects.all()
    if status:
        qs = qs.filter(status=status)
    if equipment_location:
        qs = qs.filter(equipment__location=equipment_location)
    if start_date and end_date:
        qs = qs.filter(scheduled_date__range=(start_date, end_date))
    elif start_date:
        qs = qs.filter(scheduled_date__gte=start_date)
    elif end_date:
        qs = qs.filter(scheduled_date__lte=end_date)
    return [_to_domain(obj) for obj in qs]


def list_history(work_order_id: int) -> List[WorkOrderHistory]:
    qs = WorkOrderHistoryModel.objects.filter(work_order_id=work_order_id).order_by(
        "-changed_at"
    )
    return [_history_to_domain(obj) for obj in qs]


def list_today(user_id: int, target_date: date) -> List[WorkOrder]:
    qs = WorkOrderModel.objects.filter(
        created_by_id=user_id, scheduled_date=target_date
    )
    return [_to_domain(obj) for obj in qs]


def execute(work_order_id: int, assignee: User) -> WorkOrder:
    """Finalize a work order execution."""
    obj = WorkOrderModel.objects.get(id=work_order_id)
    if obj.created_by_id != assignee.id:
        raise PermissionError("User is not the assignee")
    if obj.status != "Em Execução":
        raise ValueError("Work order not in progress")

    WorkOrderHistoryModel.objects.create(
        work_order=obj,
        old_status=obj.status,
        new_status="Concluída",
        changed_by=assignee,
    )

    obj.status = "Concluída"
    if obj.completed_date is None:
        obj.completed_date = date.today()
        send_work_order_completed(obj)
    obj.save()
    return _to_domain(obj)


class ConcurrencyError(Exception):
    """Raised when revision check fails."""


class InvalidTransitionError(Exception):
    """Raised when an invalid status transition is attempted."""


class WorkOrderService:
    """Service for work order state transitions."""

    _valid_transitions = {
        WorkOrderStatus.OPEN: {
            WorkOrderStatus.IN_PROGRESS,
            WorkOrderStatus.WAITING,
            WorkOrderStatus.DONE,
        },
        WorkOrderStatus.IN_PROGRESS: {WorkOrderStatus.WAITING, WorkOrderStatus.DONE},
        WorkOrderStatus.WAITING: {WorkOrderStatus.IN_PROGRESS, WorkOrderStatus.DONE},
    }

    def change_status(
        self,
        wo: WorkOrderModel,
        target: WorkOrderStatus,
        actor: User,
        expected_revision: int,
    ) -> WorkOrder:
        """Change status with optimistic locking and audit."""

        if wo.revision != expected_revision:
            raise ConcurrencyError()
        if target not in self._valid_transitions.get(WorkOrderStatus(wo.status), set()):
            raise InvalidTransitionError()

        prev_status = wo.status
        wo.status = target.value
        wo.revision += 1
        wo.save(update_fields=["status", "revision"])
        WorkOrderHistoryModel.objects.create(
            work_order=wo,
            old_status=prev_status,
            new_status=wo.status,
            changed_by=actor,
        )
        return _to_domain(wo)


work_order_state_machine = WorkOrderService()
