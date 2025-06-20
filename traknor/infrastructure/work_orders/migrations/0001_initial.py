from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WorkOrder",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("equipment", models.ForeignKey(on_delete=models.deletion.CASCADE, to="infra_equipment.EquipmentModel")),
                ("status", models.CharField(choices=[("Aberta", "Aberta"), ("Em Execução", "Em Execução"), ("Em Espera", "Em Espera"), ("Concluída", "Concluída")], max_length=20)),
                ("priority", models.CharField(choices=[("Alta", "Alta"), ("Média", "Média"), ("Baixa", "Baixa")], max_length=20)),
                ("scheduled_date", models.DateField(blank=True, null=True)),
                ("completed_date", models.DateField(blank=True, null=True)),
                ("created_by", models.ForeignKey(on_delete=models.deletion.CASCADE, to="infra_accounts.User")),
                ("description", models.TextField()),
                ("cost", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
