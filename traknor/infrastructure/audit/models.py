"""Audit log persistence models."""

from django.db import models

from traknor.infrastructure.accounts.user import User


class AuditLog(models.Model):
    """Store user actions for auditing."""

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    resource = models.CharField(max_length=255)
    payload = models.JSONField(default=dict)
    ip = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "infra_audit"
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
