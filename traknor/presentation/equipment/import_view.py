from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from traknor.application.services.equipment_importer import import_from_csv


class EquipmentImportView(APIView):
    """Import equipments from a CSV file."""

    def post(self, request):
        csv_file = request.FILES.get("file")
        if csv_file is None:
            return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        created, errors = import_from_csv(csv_file)
        status_code = status.HTTP_200_OK if not errors else status.HTTP_400_BAD_REQUEST
        return Response({"created": created, "errors": errors}, status=status_code)
