import uuid

from django.db import models

from traknor.infrastructure.equipment.models import EquipmentModel


class AssetModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=30, unique=True)
    model = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE)
    location = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pragma: no cover
        return self.tag
