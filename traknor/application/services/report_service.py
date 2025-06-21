from __future__ import annotations

from datetime import datetime
from typing import Sequence

from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.work_orders.models import WorkOrder


class ReportService:
    """Service to generate datasets for reports."""

    @staticmethod
    def get_dataset(
        report_type: str,
        *,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> Sequence[dict]:
        """Retrieve dataset by type and date range."""
        if report_type == "equipment":
            qs = EquipmentModel.objects.all()
            if from_date:
                qs = qs.filter(created_at__date__gte=from_date.date())
            if to_date:
                qs = qs.filter(created_at__date__lte=to_date.date())
            return list(
                qs.values(
                    "id",
                    "name",
                    "description",
                    "type",
                    "location",
                    "criticality",
                    "status",
                )
            )
        if report_type == "workorder":
            qs = WorkOrder.objects.all()
            if from_date:
                qs = qs.filter(created_at__date__gte=from_date.date())
            if to_date:
                qs = qs.filter(created_at__date__lte=to_date.date())
            return list(
                qs.values(
                    "id",
                    "equipment__name",
                    "description",
                    "status",
                    "created_at",
                    "completed_date",
                )
            )
        raise ValueError("invalid type")
