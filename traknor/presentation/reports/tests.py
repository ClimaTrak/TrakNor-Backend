import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_missing_type_returns_400(client):
    url = reverse("reports")
    response = client.get(url)
    assert response.status_code == 400


def test_equipment_pdf(client):
    url = reverse("reports") + "?type=equipment"
    response = client.get(url)
    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"
