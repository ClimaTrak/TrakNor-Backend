from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from traknor.application.services.dashboard_service import get_dashboard_summary


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = get_dashboard_summary()
        return Response(summary)
