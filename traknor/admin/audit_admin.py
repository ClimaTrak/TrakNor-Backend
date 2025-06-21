"""Admin configuration for AuditLog model."""  # pragma: no cover

from django.contrib import admin

from traknor.infrastructure.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_filter = ("user", "action", "created_at")
    search_fields = ("action", "resource")
    readonly_fields = ("payload", "ip", "created_at")
