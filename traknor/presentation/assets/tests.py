import pytest
from django.urls import reverse

from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.assets.models import AssetModel

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


def _create_asset(model, tag="TAG01"):
    return AssetModel.objects.create(
        name="Unit", tag=tag, model=model, location={"room": "1"}
    )


def test_crud_operations(client):
    model = _create_model()
    asset = _create_asset(model, "T1")

    # list
    resp = client.get(reverse("asset-list"))
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # retrieve
    resp = client.get(reverse("asset-detail", args=[asset.id]))
    assert resp.status_code == 200
    assert resp.json()["tag"] == "T1"

    # update success
    data = {"name": "U2", "tag": "T2", "model": model.id, "location": {"r": "2"}}
    resp = client.put(
        reverse("asset-detail", args=[asset.id]),
        data,
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.json()["tag"] == "T2"

    # update duplicate tag
    _create_asset(model, "T3")
    resp = client.put(
        reverse("asset-detail", args=[asset.id]),
        {"tag": "T3"},
        content_type="application/json",
    )
    assert resp.status_code == 422

    # delete
    resp = client.delete(reverse("asset-detail", args=[asset.id]))
    assert resp.status_code == 204
    assert not AssetModel.objects.filter(id=asset.id).exists()
