from uuid import uuid4

from django.db import models

from django.utils import timezone

from traknor.domain.constants import WorkOrderStatus
from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.equipment.models import EquipmentModel


class WorkOrderQuerySet(models.QuerySet["WorkOrder"]):
    """Custom queryset with helpers for soft delete."""

    def alive(self) -> models.QuerySet["WorkOrder"]:
        return self.filter(deleted_at__isnull=True)

    def deleted(self) -> models.QuerySet["WorkOrder"]:
        return self.exclude(deleted_at__isnull=True)


class WorkOrderManager(models.Manager["WorkOrder"]):
    """Manager applying the alive filter by default."""

    def get_queryset(self) -> WorkOrderQuerySet:  # type: ignore[override]
        return WorkOrderQuerySet(self.model, using=self._db).alive()

    def all_with_deleted(self) -> WorkOrderQuerySet:
        return WorkOrderQuerySet(self.model, using=self._db)


class WorkOrder(models.Model):
    STATUS_CHOICES = [(status.value, status.value) for status in WorkOrderStatus]

    PRIORITY_CHOICES = [
        ("Alta", "Alta"),
        ("Média", "Média"),
        ("Baixa", "Baixa"),
    ]

    code = models.UUIDField(default=uuid4, unique=True, editable=False)
    equipment = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=WorkOrderStatus.OPEN
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    scheduled_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revision = models.PositiveIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = WorkOrderManager()

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return str(self.code)

    def delete(self, using=None, keep_parents=False) -> None:  # type: ignore[override]
        """Soft delete the work order."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])
