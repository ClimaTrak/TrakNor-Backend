from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from traknor.application.services import (
    execute_order,
    list_today_orders,
    work_order_service,
)
from traknor.infrastructure.work_orders.models import WorkOrder as WorkOrderModel


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


class OpenOrdersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = request.query_params.get("limit")
        offset = request.query_params.get("offset")
        date_from = request.query_params.get("dateFrom")
        date_to = request.query_params.get("dateTo")

        try:
            limit = int(limit) if limit else 100
            offset = int(offset) if offset else 0
            date_from = date.fromisoformat(date_from) if date_from else None
            date_to = date.fromisoformat(date_to) if date_to else None
        except ValueError:
            return Response({"error": "Invalid parameters"}, status=400)

        orders = work_order_service.list_by_filter(
            status="Aberta", start_date=date_from, end_date=date_to
        )
        subset = orders[offset : offset + limit]
        data = [
            {
                "id": wo.id,
                "number": str(wo.code),
                "status": wo.status,
                "description": wo.description,
                "assignee": wo.created_by_id,
            }
            for wo in subset
        ]
        return Response(data)


class OsExecuteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            wo = execute_order(int(pk), request.user)
        except WorkOrderModel.DoesNotExist:
            return Response(status=404)
        except PermissionError:
            return Response(status=403)
        except ValueError:
            return Response({"error": "Invalid status"}, status=400)

        duration = 0
        if wo.completed_date and wo.scheduled_date:
            duration = (wo.completed_date - wo.scheduled_date).days
        return Response({"id": wo.id, "status": wo.status, "duration": duration})
