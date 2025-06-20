"""API views for authentication."""

from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from traknor.application.services.auth_service import AuthService
from traknor.infrastructure.serializers.user_serializer import (
    UserRegisterSerializer,
)


class LoginView(TokenObtainPairView):
    """Return JWT tokens for a valid user."""


class RefreshView(TokenRefreshView):
    """Refresh access token."""


class RegisterView(generics.CreateAPIView):
    """Create a new user."""

    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")
        user = AuthService.create_user(password=password, **serializer.validated_data)
        serializer.instance = user
