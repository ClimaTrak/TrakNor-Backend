from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("infra_accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                (
                    "role",
                    models.CharField(
                        max_length=20,
                        choices=[
                            ("ADMIN", "Admin"),
                            ("TECH", "T\u00e9cnico"),
                            ("CLIENT", "Cliente"),
                        ],
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        to="auth.group",
                        blank=True,
                        related_name="user_set",
                        related_query_name="user",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        to="auth.permission",
                        blank=True,
                        related_name="user_set",
                        related_query_name="user",
                    ),
                ),
            ],
        ),
    ]
