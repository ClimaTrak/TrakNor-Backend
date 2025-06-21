import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def _register_user(client, email="user@example.com", password="pass1234"):
    url = reverse("accounts:register")
    data = {
        "email": email,
        "first_name": "Test",
        "last_name": "User",
        "role": "technician",
        "password": password,
    }
    return client.post(url, data, content_type="application/json")


def test_user_registration(client):
    response = _register_user(client)
    assert response.status_code == 201
    assert response.json()["email"] == "user@example.com"


def test_login_and_refresh(client):
    _register_user(client)
    login_url = reverse("accounts:login")
    login_resp = client.post(
        login_url,
        {"email": "user@example.com", "password": "pass1234"},
        content_type="application/json",
    )
    assert login_resp.status_code == 200
    data = login_resp.json()
    assert "access" in data and "refresh" in data

    refresh_url = reverse("accounts:token_refresh")
    refresh_resp = client.post(
        refresh_url, {"refresh": data["refresh"]}, content_type="application/json"
    )
    assert refresh_resp.status_code == 200
    assert "access" in refresh_resp.json()
