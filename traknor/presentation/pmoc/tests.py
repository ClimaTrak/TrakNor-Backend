import pytest
from django.urls import reverse

from traknor.infrastructure.assets.models import AssetModel
from traknor.infrastructure.equipment.models import EquipmentModel

pytestmark = pytest.mark.django_db


def _create_asset():
    equip = EquipmentModel.objects.create(
        name="EQ1",
        description="",
        type="Split",
        location="L",
        criticality="Média",
        status="Operacional",
    )
    asset = AssetModel.objects.create(
        name="Asset",
        tag="TAG1",
        model=equip,
        location={"room": "1"},
    )
    return asset


def test_generate_pmoc(client):
    asset = _create_asset()
    url = reverse("pmoc:generate")
    resp = client.post(
        url,
        {"assetId": str(asset.id), "frequency": "monthly"},
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert len(resp.json()["schedule"]) == 12


def test_generate_pmoc_asset_not_found(client):
    url = reverse("pmoc:generate")
    resp = client.post(
        url,
        {"assetId": "00000000-0000-0000-0000-000000000000", "frequency": "monthly"},
        content_type="application/json",
    )
    assert resp.status_code == 404
