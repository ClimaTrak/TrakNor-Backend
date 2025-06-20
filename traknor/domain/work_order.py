from dataclasses import dataclass
from datetime import date
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
