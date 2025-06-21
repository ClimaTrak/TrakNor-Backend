"""Middleware for auditing user actions."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse

from traknor.infrastructure.audit.models import AuditLog


class AuditMiddleware:
    """Persist an audit log entry for mutating requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        body = getattr(request, "data", {})
        response = self.get_response(request)
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            AuditLog.objects.create(
                user=request.user
                if getattr(request, "user", None) and request.user.is_authenticated
                else None,
                action=f"{request.method} {request.path}",
                resource=request.path,
                payload=body,
                ip=request.META.get("REMOTE_ADDR"),
            )
        return response
