import pytest
from django.urls import reverse

from traknor.infrastructure.equipment.models import EquipmentModel

pytestmark = pytest.mark.django_db


def _create_model():
    return EquipmentModel.objects.create(
        name="Chiller 1000",
        description="",
        type="Chiller",
        location="Plant",
        criticality="Alta",
        status="Operacional",
    )


def test_create_asset(client):
    model = _create_model()
    url = reverse("asset-list")
    data = {
        "name": "Unit 1",
        "tag": "TAG01",
        "model": model.id,
        "location": {"room": "1A"},
    }
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 201
    assert "assetId" in response.json()


def test_duplicate_tag(client):
    model = _create_model()
    url = reverse("asset-list")
    data = {
        "name": "Unit 1",
        "tag": "TAG01",
        "model": model.id,
        "location": {"room": "1A"},
    }
    client.post(url, data, content_type="application/json")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 422
    assert response.json()["error"] == "TAG exists"
