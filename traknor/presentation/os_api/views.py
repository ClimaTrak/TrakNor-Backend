from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from traknor.application.services import list_today_orders


class OsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assignee = request.query_params.get("assignee")
        date_param = request.query_params.get("date")

        if assignee == "me":
            user_id = request.user.id
        else:
            try:
                user_id = int(assignee)
            except (TypeError, ValueError):
                return Response({"error": "Invalid assignee"}, status=400)

        if date_param == "today":
            target_date = date.today()
        else:
            try:
                target_date = date.fromisoformat(date_param)
            except (TypeError, ValueError):
                return Response({"error": "Invalid date"}, status=400)

        orders = list_today_orders(user_id, target_date)
        data = [
            {
                "id": wo.id,
                "number": str(wo.code),
                "status": wo.status,
                "description": wo.description,
                "assignee": wo.created_by_id,
            }
            for wo in orders
        ]
        return Response(data)
