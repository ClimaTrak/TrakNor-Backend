from rest_framework import status, viewsets
from rest_framework.response import Response

from traknor.application.services.asset_service import (
    DuplicateTagError,
)
from traknor.application.services.asset_service import (
    create as create_asset,
)
from traknor.infrastructure.assets.serializers import AssetSerializer


class AssetViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = AssetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            asset = create_asset(serializer.validated_data)
        except DuplicateTagError:
            return Response({"error": "TAG exists"}, status=422)
        return Response({"assetId": str(asset.id)}, status=status.HTTP_201_CREATED)
