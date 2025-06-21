from rest_framework import viewsets
from rest_framework.response import Response

from traknor.application.services import work_order_service
from traknor.infrastructure.work_orders.serializers import WorkOrderSerializer


class WorkOrderViewSet(viewsets.ViewSet):
    """Interface de listagem, criação, visualização e atualização de ordens de serviço. (sem exclusão)"""

    def list(self, request):
        work_orders = work_order_service.list_by_filter(
            status=request.query_params.get("status"),
            equipment_location=request.query_params.get("equipment"),
        )
        data = [wo.__dict__ for wo in work_orders]
        return Response(data)

    def create(self, request):
        serializer = WorkOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wo = work_order_service.create(serializer.validated_data)
        return Response(wo.__dict__, status=201)

    def retrieve(self, request, pk=None):
        work_orders = work_order_service.list_by_filter()
        for wo in work_orders:
            if str(wo.id) == str(pk):
                return Response(wo.__dict__)
        return Response(status=404)

    def update(self, request, pk=None):
        serializer = WorkOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wo = work_order_service.update_status(int(pk), serializer.validated_data["status"])
        return Response(wo.__dict__)
