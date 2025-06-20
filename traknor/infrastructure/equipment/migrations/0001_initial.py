from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='EquipmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('Split', 'Split'), ('Fancoil', 'Fancoil'), ('Chiller', 'Chiller')], max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('criticality', models.CharField(choices=[('Alta', 'Alta'), ('Média', 'Média'), ('Baixa', 'Baixa')], max_length=50)),
                ('status', models.CharField(choices=[('Operacional', 'Operacional'), ('Inoperante', 'Inoperante'), ('Manutenção', 'Manutenção')], max_length=50)),
            ],
        ),
    ]
