from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("infra_work_orders", "0002_workorderhistory"),
    ]

    operations = [
        migrations.AddField(
            model_name="workorder",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="workorder",
            name="revision",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="workorder",
            name="status",
            field=models.CharField(
                default="OPEN",
                choices=[
                    ("OPEN", "OPEN"),
                    ("IN_PROGRESS", "IN_PROGRESS"),
                    ("WAITING", "WAITING"),
                    ("DONE", "DONE"),
                ],
                max_length=20,
            ),
        ),
    ]

