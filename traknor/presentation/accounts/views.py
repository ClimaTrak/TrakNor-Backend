"""API views for authentication."""

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings

from traknor.application.services.auth_service import AuthService
from traknor.application.services import twofa_service
from traknor.infrastructure.serializers.user_serializer import (
    UserRegisterSerializer,
)


class LoginView(TokenObtainPairView):
    """Return JWT tokens or temp token when 2FA is enabled."""

    def post(self, request, *args, **kwargs):  # pragma: no cover - thin wrapper
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if settings.ENABLE_2FA and getattr(user, "is_2fa_enabled", False):
            temp = twofa_service.generate_temp_token(user)
            return Response({"temp_token": temp}, status=202)
        return Response(serializer.validated_data)


class RefreshView(TokenRefreshView):
    """Refresh access token."""


class RegisterView(generics.CreateAPIView):
    """Create a new user."""

    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")
        user = AuthService.create_user(password=password, **serializer.validated_data)
        serializer.instance = user
