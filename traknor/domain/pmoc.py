from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass
class PmocSchedule:
    id: UUID
    asset_id: UUID
    date: date
    status: str
    created_at: datetime
