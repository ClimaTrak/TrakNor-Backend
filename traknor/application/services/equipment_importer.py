import csv
import io
from typing import List, Dict, Tuple

from django.core.exceptions import ValidationError

from traknor.infrastructure.equipment.models import EquipmentModel

HEADERS = [
    "name",
    "description",
    "type",
    "location",
    "criticality",
    "status",
]


def import_from_csv(file) -> Tuple[int, List[Dict]]:
    """Import equipments from a CSV file.

    Parameters
    ----------
    file: UploadedFile or file-like object opened in binary mode
        CSV file with UTF-8 encoding.

    Returns
    -------
    Tuple[int, List[Dict]]
        Number of created objects and a list of errors per line.
    """
    data = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(data))

    if reader.fieldnames != HEADERS:
        return 0, [{"line": 1, "errors": "Invalid headers"}]

    objects = []
    errors: List[Dict] = []

    for line_num, row in enumerate(reader, start=2):
        obj = EquipmentModel(**row)
        try:
            obj.full_clean()
            objects.append(obj)
        except ValidationError as e:
            errors.append({"line": line_num, "errors": e.message_dict})

    if errors:
        return 0, errors

    EquipmentModel.objects.bulk_create(objects)
    return len(objects), []
