from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass
class WorkOrder:
    id: int | None
    code: UUID
    equipment_id: int
    status: str
    priority: str
    scheduled_date: date | None
    completed_date: date | None
    created_by_id: int
    description: str
    cost: float


@dataclass
class WorkOrderHistory:
    """Status change event for a WorkOrder."""

    id: int | None
    work_order_id: int
    old_status: str
    new_status: str
    changed_by_id: int
    changed_at: datetime
