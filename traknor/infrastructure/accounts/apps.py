from django.apps import AppConfig


class AccountsInfraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "traknor.infrastructure.accounts"
    label = "infra_accounts"
