from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Asset:
    id: UUID
    name: str
    tag: str
    model_id: int
    location: dict
    created_at: datetime
