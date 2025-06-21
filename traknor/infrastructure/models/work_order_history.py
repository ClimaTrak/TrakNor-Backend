from django.db import models

from traknor.infrastructure.work_orders.models import WorkOrder
from traknor.infrastructure.accounts.user import User


class WorkOrderHistory(models.Model):
    """Persistence model for changes in WorkOrder status."""

    work_order = models.ForeignKey(
        WorkOrder, on_delete=models.CASCADE, related_name="history"
    )
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "infra_work_orders"
        ordering = ["-changed_at"]
