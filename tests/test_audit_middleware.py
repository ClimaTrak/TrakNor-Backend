import pytest
from django.urls import reverse

from traknor.infrastructure.audit.models import AuditLog

pytestmark = pytest.mark.django_db


def test_audit_log_created(client):
    data = {
        "email": "a@example.com",
        "first_name": "A",
        "last_name": "U",
        "role": "technician",
        "password": "pass",
    }
    client.post(reverse("accounts:register"), data, content_type="application/json")
    log = AuditLog.objects.latest("id")
    assert log.action == "POST /api/auth/register/"
    assert log.resource == "/api/auth/register/"
    assert AuditLog.objects.count() == 1
