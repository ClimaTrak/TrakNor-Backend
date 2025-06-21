# Application services

from .asset_service import create as create_asset, DuplicateTagError

__all__ = ["create_asset", "DuplicateTagError"]
