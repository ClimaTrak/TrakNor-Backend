import pytest
from django.urls import reverse
from django.template import TemplateDoesNotExist

from traknor.infrastructure.accounts.user import User

pytestmark = pytest.mark.django_db


def _create_user():
    return User.objects.create_user(
        email="user@example.com",
        password="pass",
        first_name="Test",
        last_name="User",
        role="technician",
    )


def _auth_headers(client):
    login_resp = client.post(
        reverse("accounts:login"),
        {"email": "user@example.com", "password": "pass"},
        content_type="application/json",
    )
    token = login_resp.json()["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


def test_missing_type_returns_400(client):
    _create_user()
    headers = _auth_headers(client)
    url = reverse("reports")
    response = client.get(url, **headers)
    assert response.status_code == 400


def test_equipment_pdf(client):
    _create_user()
    headers = _auth_headers(client)
    url = reverse("reports") + "?type=equipment"
    with pytest.raises(TemplateDoesNotExist):
        client.get(url, **headers)
