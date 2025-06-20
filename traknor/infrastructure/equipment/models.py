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

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    location = models.CharField(max_length=255)
    criticality = models.CharField(max_length=50, choices=CRITICALITY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self) -> str:
        return self.name
