from rest_framework import status, viewsets
from rest_framework.response import Response

from traknor.application.services.equipment_service import (
    create_equipment,
    list_equipment,
)
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.equipment.serializers import EquipmentSerializer
from traknor.presentation.core.mixins import SpectacularMixin


class EquipmentViewSet(SpectacularMixin, viewsets.ModelViewSet):
    """ViewSet providing list, create and CSV import operations for equipment.

    CSV import is handled by :class:`EquipmentImportView` at ``/api/equipment/import/``.
    """

    serializer_class = EquipmentSerializer
    queryset = EquipmentModel.objects.all()
    lookup_field = "id"
    lookup_value_regex = r"\d+"

    def list(self, request):
        equipments = list_equipment()
        data = [e.__dict__ for e in equipments]
        return Response(data)

    def create(self, request):
        serializer = EquipmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        equipment = create_equipment(serializer.validated_data)
        return Response(equipment.__dict__, status=status.HTTP_201_CREATED)
