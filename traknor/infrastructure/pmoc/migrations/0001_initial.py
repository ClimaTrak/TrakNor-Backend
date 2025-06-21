from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("infra_assets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PmocScheduleModel",
            fields=[
                (
                    "id",
                    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
                ),
                (
                    "asset",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, to="infra_assets.assetmodel"),
                ),
                ("date", models.DateField()),
                ("status", models.CharField(max_length=20, default="pending")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"app_label": "infra_pmoc"},
        ),
    ]
