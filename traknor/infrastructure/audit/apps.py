from django.apps import AppConfig


class AuditInfraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "traknor.infrastructure.audit"
    label = "infra_audit"
