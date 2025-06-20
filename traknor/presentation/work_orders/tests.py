import pytest
from datetime import date

from traknor.application.services import work_order_service
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.models.user import User

pytestmark = pytest.mark.django_db


def _create_basic_objects():
    user = User.objects.create_user(
        email="tech@example.com",
        password="pass",
        first_name="Tech",
        last_name="User",
        role="TECH",
    )
    equip = EquipmentModel.objects.create(
        name="EQ1",
        description="",
        type="Split",
        location="Room",
        criticality="Média",
        status="Operacional",
    )
    return user, equip


def test_status_transitions():
    user, equip = _create_basic_objects()
    wo = work_order_service.create(
        {
            "equipment": equip,
            "priority": "Alta",
            "scheduled_date": date.today(),
            "created_by": user,
            "description": "Check",
            "cost": 0,
        }
    )
    assert wo.status == "Aberta"
    wo = work_order_service.update_status(wo.id, "Em Execução")
    assert wo.status == "Em Execução"
    wo = work_order_service.update_status(wo.id, "Concluída")
    assert wo.status == "Concluída"
    with pytest.raises(ValueError):
        work_order_service.update_status(wo.id, "Aberta")


def test_list_by_filter():
    user, equip = _create_basic_objects()
    other = EquipmentModel.objects.create(
        name="EQ2",
        description="",
        type="Split",
        location="Other",
        criticality="Média",
        status="Operacional",
    )
    work_order_service.create(
        {
            "equipment": equip,
            "priority": "Alta",
            "scheduled_date": date.today(),
            "created_by": user,
            "description": "A",
            "cost": 0,
        }
    )
    work_order_service.create(
        {
            "equipment": other,
            "priority": "Alta",
            "scheduled_date": date.today(),
            "created_by": user,
            "description": "B",
            "cost": 0,
        }
    )
    res = work_order_service.list_by_filter(equipment_location="Room")
    assert len(res) == 1
