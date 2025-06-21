from django.db import models


class EquipmentModel(models.Model):
    TYPE_CHOICES = [
        ("Split", "Split"),
        ("Fancoil", "Fancoil"),
        ("Chiller", "Chiller"),
    ]

    CRITICALITY_CHOICES = [
        ("Alta", "Alta"),
        ("Média", "Média"),
        ("Baixa", "Baixa"),
    ]

    STATUS_CHOICES = [
        ("Operacional", "Operacional"),
        ("Inoperante", "Inoperante"),
        ("Manutenção", "Manutenção"),
    ]

    name: str = models.CharField(max_length=255)  # type: ignore[assignment]
    description: str = models.TextField(blank=True)  # type: ignore[assignment]
    type: str = models.CharField(max_length=50, choices=TYPE_CHOICES)  # type: ignore[assignment]
    location: str = models.CharField(max_length=255)  # type: ignore[assignment]
    criticality: str = models.CharField(max_length=50, choices=CRITICALITY_CHOICES)  # type: ignore[assignment]
    status: str = models.CharField(max_length=50, choices=STATUS_CHOICES)  # type: ignore[assignment]

    def __str__(self) -> str:
        return self.name
