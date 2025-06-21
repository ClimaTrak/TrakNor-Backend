"""Custom user model implementation."""

from __future__ import annotations

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from typing import Any
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager["User"]):
    """Manager for custom User model."""

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "User":
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model using email as username."""

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TECHNICIAN = "TECH", "Técnico"
        CLIENT = "CLIENT", "Cliente"

    email: str = models.EmailField(unique=True)  # type: ignore[assignment]
    first_name: str = models.CharField(max_length=150)  # type: ignore[assignment]
    last_name: str = models.CharField(max_length=150)  # type: ignore[assignment]
    role: str = models.CharField(max_length=20, choices=Roles.choices)  # type: ignore[assignment]
    is_active: bool = models.BooleanField(default=True)  # type: ignore[assignment]
    is_staff: bool = models.BooleanField(default=False)  # type: ignore[assignment]
    date_joined: timezone.datetime = models.DateTimeField(default=timezone.now)  # type: ignore[assignment]

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    class Meta:
        app_label = "infra_accounts"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.email
