from __future__ import annotations

from datetime import date
from typing import List
from uuid import UUID

from traknor.domain.pmoc import PmocSchedule
from traknor.infrastructure.assets.models import AssetModel
from traknor.infrastructure.pmoc.models import PmocScheduleModel

FREQUENCY_MONTHS = {
    "monthly": 1,
    "bimonthly": 2,
    "quarterly": 3,
    "semester": 6,
    "yearly": 12,
}


def _add_months(d: date, months: int) -> date:
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    day = min(
        d.day,
        [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
         31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1],
    )
    return date(year, month, day)


class AssetNotFoundError(Exception):
    pass


class InvalidFrequencyError(Exception):
    pass


def generate(
    asset_id: UUID, frequency: str, start_date: date | None = None
) -> List[PmocSchedule]:
    if frequency not in FREQUENCY_MONTHS:
        raise InvalidFrequencyError("Invalid frequency")
    try:
        asset = AssetModel.objects.get(id=asset_id)
    except AssetModel.DoesNotExist as exc:  # pragma: no cover
        raise AssetNotFoundError("Asset not found") from exc

    start_date = start_date or date.today()
    step = FREQUENCY_MONTHS[frequency]
    schedule: List[PmocSchedule] = []
    for i in range(12):
        current = _add_months(start_date, step * i)
        obj = PmocScheduleModel.objects.create(
            asset=asset, date=current, status="pending"
        )
        schedule.append(
            PmocSchedule(
                id=obj.id,
                asset_id=asset.id,
                date=obj.date,
                status=obj.status,
                created_at=obj.created_at,
            )
        )
    return schedule
