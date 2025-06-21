from __future__ import annotations

from datetime import datetime
from typing import Any

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from traknor.application.services.report_service import ReportService
from traknor.infrastructure.reports.excel_renderer import ExcelRenderer
from traknor.infrastructure.reports.pdf_renderer import PdfRenderer


class ReportView(APIView):
    """Generate equipment or work order reports in PDF or Excel."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        report_type = request.query_params.get("type")
        if not report_type:
            return Response({"detail": "type is required"}, status=400)
        format_ = request.query_params.get("format", "pdf")
        try:
            from_date = (
                datetime.fromisoformat(request.query_params["from"])
                if "from" in request.query_params
                else None
            )
            to_date = (
                datetime.fromisoformat(request.query_params["to"])
                if "to" in request.query_params
                else None
            )
        except ValueError:
            return Response({"detail": "invalid date"}, status=400)

        try:
            rows = ReportService.get_dataset(
                report_type, from_date=from_date, to_date=to_date
            )
        except ValueError:
            return Response({"detail": "invalid type"}, status=400)

        context: dict[str, Any] = {"title": "Report", "rows": rows}
        if format_ == "xlsx":
            data = ExcelRenderer.render(context, sheet_name="Report")
            return Response(
                data,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        data = PdfRenderer.render(
            context,
            template_name=f"reports/{report_type}_report.html",
        )
        return Response(data, content_type="application/pdf")
