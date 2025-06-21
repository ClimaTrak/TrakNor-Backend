from enum import Enum


class WorkOrderStatus(str, Enum):
    """Possible statuses for a work order."""

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING = "WAITING"
    DONE = "DONE"
