import pytest
from django.urls import reverse

from traknor.infrastructure.accounts.user import User

pytestmark = pytest.mark.django_db


def test_profile_role_field(client):
    User.objects.create_user(
        email="tech@example.com",
        password="pass",
        first_name="Tech",
        last_name="User",
        role="technician",
    )
    login_resp = client.post(
        reverse("accounts:login"),
        {"email": "tech@example.com", "password": "pass"},
        content_type="application/json",
    )
    token = login_resp.json()["access"]

    resp = client.get("/api/profile/", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert resp.status_code == 200
    assert resp.json()["role"] == "technician"
