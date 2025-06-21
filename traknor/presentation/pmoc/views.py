from rest_framework.views import APIView
from rest_framework.response import Response

from traknor.infrastructure.pmoc.serializers import GeneratePmocSerializer
from traknor.application.services import generate_pmoc
from traknor.application.services.pmoc_service import AssetNotFoundError


class PmocGenerateView(APIView):
    def post(self, request):
        serializer = GeneratePmocSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            schedule = generate_pmoc(
                asset_id=data["assetId"],
                frequency=data["frequency"],
                start_date=data.get("startDate"),
            )
        except AssetNotFoundError:
            return Response({"error": "Asset not found"}, status=404)

        return Response({"schedule": [s.date.isoformat() for s in schedule]}, status=201)
