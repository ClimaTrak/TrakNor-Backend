from django.apps import AppConfig


class WorkOrdersInfraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "traknor.infrastructure.work_orders"
    label = "infra_work_orders"
