from typing import List

from traknor.domain.equipment import Equipment
from traknor.infrastructure.equipment.models import EquipmentModel


def create_equipment(data: dict) -> Equipment:
    obj = EquipmentModel.objects.create(**data)
    return Equipment(
        name=obj.name,
        description=obj.description,
        type=obj.type,
        location=obj.location,
        criticality=obj.criticality,
        status=obj.status,
    )


def list_equipment() -> List[Equipment]:
    equipments = []
    for obj in EquipmentModel.objects.all():
        equipments.append(
            Equipment(
                name=obj.name,
                description=obj.description,
                type=obj.type,
                location=obj.location,
                criticality=obj.criticality,
                status=obj.status,
            )
        )
    return equipments
