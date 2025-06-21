from uuid import uuid4

from django.db import models

from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.equipment.models import EquipmentModel


class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ("Aberta", "Aberta"),
        ("Em Execução", "Em Execução"),
        ("Em Espera", "Em Espera"),
        ("Concluída", "Concluída"),
    ]

    PRIORITY_CHOICES = [
        ("Alta", "Alta"),
        ("Média", "Média"),
        ("Baixa", "Baixa"),
    ]

    code = models.UUIDField(default=uuid4, unique=True, editable=False)
    equipment = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    scheduled_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return str(self.code)
