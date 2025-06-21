"""Application services for authentication and user management."""

from __future__ import annotations

from django.contrib.auth import get_user_model

User = get_user_model()


class AuthService:
    """Service layer for authentication related actions."""

    @staticmethod
    def create_user(
        *, email: str, password: str, first_name: str, last_name: str, role: str
    ) -> User:
        """Create a regular user using the configured manager."""

        return User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
