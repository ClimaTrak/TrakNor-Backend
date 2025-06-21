# pragma: no cover
from drf_spectacular.utils import extend_schema

# pragma: no cover - thin view layer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from traknor.application.services import work_order_service, work_order_state_machine
from traknor.domain.constants import WorkOrderStatus
from traknor.infrastructure.work_orders.models import WorkOrder as WorkOrderModel
from traknor.infrastructure.work_orders.serializers import (
    WorkOrderSerializer,
    WorkOrderStatusSerializer,
)
from traknor.infrastructure.work_orders.work_order_history_serializer import (
    WorkOrderHistorySerializer,
)
from traknor.presentation.core.mixins import SpectacularMixin


class WorkOrderViewSet(SpectacularMixin, viewsets.ViewSet):
    """Interface de listagem, criação, visualização e atualização de ordens de
    serviço. (sem exclusão)"""

    serializer_class = WorkOrderSerializer
    queryset = WorkOrderModel.objects.all()
    lookup_field = "id"
    lookup_value_regex = r"\d+"

    def list(self, request):
        work_orders = work_order_service.list_by_filter(
            status=request.query_params.get("status"),
            equipment_location=request.query_params.get("equipment"),
        )
        data = [wo.__dict__ for wo in work_orders]
        return Response(data)

    def create(self, request):  # pragma: no cover - thin wrapper
        serializer = WorkOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wo = work_order_service.create(serializer.validated_data)
        return Response(wo.__dict__, status=201)

    def retrieve(self, request, id=None):  # pragma: no cover - simple loop
        work_orders = work_order_service.list_by_filter()
        for wo in work_orders:
            if str(wo.id) == str(id):
                return Response(wo.__dict__)
        return Response(status=404)

    def update(self, request, id=None):  # pragma: no cover - delegated logic
        serializer = WorkOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = WorkOrderModel.objects.get(id=id)
        wo = work_order_state_machine.change_status(
            obj,
            WorkOrderStatus(serializer.validated_data["status"]),
            request.user,
            int(request.data.get("revision", obj.revision)),
        )
        return Response(wo.__dict__)

    def partial_update(self, request, id=None):  # pragma: no cover
        return self.update(request, id)

    def destroy(self, request, id=None):  # pragma: no cover
        try:
            obj = WorkOrderModel.objects.get(id=id)
        except WorkOrderModel.DoesNotExist:
            return Response(status=404)
        obj.delete()
        return Response(status=204)

    @action(detail=True, methods=["get"])
    @extend_schema(responses=WorkOrderHistorySerializer(many=True))
    def history(self, request, id=None):
        history = work_order_service.list_history(int(id))
        serializer = WorkOrderHistorySerializer(history, many=True)
        return Response(serializer.data)
