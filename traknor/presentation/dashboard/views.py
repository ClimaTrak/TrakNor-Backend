from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import date

from traknor.application.services.dashboard_service import (
    get_dashboard_summary,
    get_kpis,
)


class DashboardSummaryView(APIView):
    """Provide summary metrics for the dashboard."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = get_dashboard_summary()
        return Response(summary)


class KPIView(APIView):
    """Expose basic KPI metrics."""

    permission_classes = [IsAuthenticated]

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
