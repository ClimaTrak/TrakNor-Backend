from rest_framework import status, viewsets
from rest_framework.response import Response

from traknor.application.services import asset_service
from traknor.application.services.asset_service import DuplicateTagError
from traknor.infrastructure.assets.models import AssetModel
from traknor.infrastructure.assets.serializers import (
    AssetCreateSerializer,
    AssetSerializer,
    AssetUpdateSerializer,
)


class AssetViewSet(viewsets.ViewSet):
    """Provide CRUD operations for assets."""

    def list(self, request):
        assets = asset_service.list_assets()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AssetCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            asset = asset_service.create(serializer.validated_data)
        except DuplicateTagError:
            return Response({"error": "TAG exists"}, status=422)
        return Response({"assetId": str(asset.id)}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            asset = asset_service.get_asset(pk)
        except AssetModel.DoesNotExist:
            return Response(status=404)
        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = AssetUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            asset = asset_service.update_asset(pk, serializer.validated_data)
        except AssetModel.DoesNotExist:
            return Response(status=404)
        except DuplicateTagError:
            return Response({"error": "TAG exists"}, status=422)
        return Response(AssetSerializer(asset).data)

    def destroy(self, request, pk=None):
        try:
            asset_service.delete_asset(pk)
        except AssetModel.DoesNotExist:
            return Response(status=404)
        return Response(status=204)
