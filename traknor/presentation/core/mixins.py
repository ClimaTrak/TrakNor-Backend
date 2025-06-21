from typing import Type

from rest_framework.serializers import BaseSerializer


class SpectacularMixin:
    """Helpers to satisfy drf-spectacular when view is not a ``ModelViewSet``."""

    serializer_class: Type[BaseSerializer] | None = None
    queryset = None

    def get_serializer_class(self) -> Type[BaseSerializer]:
        assert self.serializer_class, (
            f"{self.__class__.__name__} must define serializer_class "
            "for OpenAPI generation."
        )
        return self.serializer_class
