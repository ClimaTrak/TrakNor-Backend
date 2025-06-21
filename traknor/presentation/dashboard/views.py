from datetime import date

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from traknor.application.services.dashboard_service import (
    get_dashboard_summary,
    get_kpis,
)
from traknor.presentation.core.mixins import SpectacularMixin

from .serializers import DashboardSummarySerializer


class DashboardSummaryView(SpectacularMixin, APIView):
    """Provide summary metrics for the dashboard."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=DashboardSummarySerializer)
    def get(self, request):
        summary = get_dashboard_summary()
        return Response(summary)


class KPIView(SpectacularMixin, APIView):
    """Expose basic KPI metrics."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=DashboardSummarySerializer)
    def get(self, request):
        try:
            from_param = request.query_params.get("from")
            to_param = request.query_params.get("to")
            eq_param = request.query_params.get("equipment_id")
            group_by = request.query_params.get("group_by")

            range_from = date.fromisoformat(from_param) if from_param else None
            range_to = date.fromisoformat(to_param) if to_param else None
            equipment_id = int(eq_param) if eq_param else None
        except ValueError:
            return Response({"error": "Invalid parameters"}, status=400)

        data = get_kpis(
            range_from=range_from,
            range_to=range_to,
            equipment_id=equipment_id,
            group_by=group_by,
        )
        return Response(data)
