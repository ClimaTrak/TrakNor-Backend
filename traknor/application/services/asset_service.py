from typing import List
from uuid import UUID

from traknor.domain.asset import Asset
from traknor.infrastructure.assets.models import AssetModel


class DuplicateTagError(Exception):
    """Raised when an asset with the provided tag already exists."""


def create(data: dict) -> Asset:
    if AssetModel.objects.filter(tag=data["tag"]).exists():
        raise DuplicateTagError("TAG exists")
    obj = AssetModel.objects.create(
        name=data["name"],
        tag=data["tag"],
        model=data["model"],
        location=data["location"],
    )
    return _to_domain(obj)


def _to_domain(obj: AssetModel) -> Asset:
    return Asset(
        id=obj.id,
        name=obj.name,
        tag=obj.tag,
        model_id=obj.model_id,
        location=obj.location,
        created_at=obj.created_at,
    )


def list_assets() -> List[Asset]:
    return [_to_domain(obj) for obj in AssetModel.objects.all()]


def get_asset(asset_id: UUID) -> Asset:
    obj = AssetModel.objects.get(id=asset_id)
    return _to_domain(obj)


def update_asset(asset_id: UUID, data: dict) -> Asset:
    obj = AssetModel.objects.get(id=asset_id)
    if "tag" in data and AssetModel.objects.exclude(id=asset_id).filter(tag=data["tag"]).exists():
        raise DuplicateTagError("TAG exists")
    for field, value in data.items():
        setattr(obj, field, value)
    obj.save()
    return _to_domain(obj)


def delete_asset(asset_id: UUID) -> None:
    obj = AssetModel.objects.get(id=asset_id)
    obj.delete()
