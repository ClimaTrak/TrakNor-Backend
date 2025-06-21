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
    return Asset(
        id=obj.id,
        name=obj.name,
        tag=obj.tag,
        model_id=obj.model_id,
        location=obj.location,
        created_at=obj.created_at,
    )
