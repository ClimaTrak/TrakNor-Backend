"""Authenticated user profile endpoint."""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from traknor.presentation.core.mixins import SpectacularMixin
from traknor.infrastructure.serializers.user_serializer import UserSerializer


class ProfileView(SpectacularMixin, generics.RetrieveAPIView):
    """Return the currently authenticated user."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
