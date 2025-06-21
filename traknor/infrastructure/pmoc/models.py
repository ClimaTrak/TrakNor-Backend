import uuid
from django.db import models

from traknor.infrastructure.assets.models import AssetModel


class PmocScheduleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(AssetModel, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "infra_pmoc"
