from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("infra_equipment", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("tag", models.CharField(max_length=30, unique=True)),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        to="infra_equipment.EquipmentModel",
                    ),
                ),
                ("location", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
