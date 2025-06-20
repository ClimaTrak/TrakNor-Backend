"""Domain entities for accounts."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """User domain entity."""

    id: int | None
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    date_joined: datetime
