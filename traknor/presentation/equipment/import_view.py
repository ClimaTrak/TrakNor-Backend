from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from traknor.application.services.equipment_importer import import_from_csv

from .serializers import (
    EquipmentImportSerializer,
    ImportResultSerializer,
)


class EquipmentImportView(GenericAPIView):
    """Import equipments from a CSV file."""

    serializer_class = EquipmentImportSerializer

    @extend_schema(
        request=EquipmentImportSerializer,
        responses=ImportResultSerializer,
    )
    def post(self, request):
        csv_file = request.FILES.get("file")
        if csv_file is None:
            return Response(
                {"detail": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created, errors = import_from_csv(csv_file)
        status_code = status.HTTP_200_OK if not errors else status.HTTP_400_BAD_REQUEST
        return Response({"created": created, "errors": errors}, status=status_code)
