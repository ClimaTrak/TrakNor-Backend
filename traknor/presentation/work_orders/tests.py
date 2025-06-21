import pytest
from datetime import date

from traknor.application.services import work_order_service
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.models.work_order_history import WorkOrderHistory
from rest_framework.test import APIClient

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


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def work_order():
    user, equip = _create_basic_objects()
    return work_order_service.create(
        {
            "equipment": equip,
            "priority": "Alta",
            "scheduled_date": date.today(),
            "created_by": user,
            "description": "Teste",
            "cost": 0,
        }
    )


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
    wo = work_order_service.update_status(wo.id, "Em Execução", user)
    assert wo.status == "Em Execução"
    wo = work_order_service.update_status(wo.id, "Concluída", user)
    assert wo.status == "Concluída"
    with pytest.raises(ValueError):
        work_order_service.update_status(wo.id, "Aberta", user)


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


def test_retrieve_work_order(api_client, work_order):
    response = api_client.get(f"/api/work-orders/{work_order.id}/")
    assert response.status_code == 200
    assert response.json()["id"] == work_order.id


def test_history_record_created():
    user, equip = _create_basic_objects()
    wo = work_order_service.create(
        {
            "equipment": equip,
            "priority": "Alta",
            "scheduled_date": date.today(),
            "created_by": user,
            "description": "Teste",
            "cost": 0,
        }
    )
    work_order_service.update_status(wo.id, "Em Execução", user)
    assert WorkOrderHistory.objects.filter(work_order_id=wo.id).count() == 1


def test_history_endpoint(api_client):
    user, equip = _create_basic_objects()
    wo = work_order_service.create(
        {
            "equipment": equip,
            "priority": "Alta",
            "scheduled_date": date.today(),
            "created_by": user,
            "description": "Teste",
            "cost": 0,
        }
    )
    work_order_service.update_status(wo.id, "Em Execução", user)
    work_order_service.update_status(wo.id, "Concluída", user)

    response = api_client.get(f"/api/work-orders/{wo.id}/history/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["new_status"] == "Concluída"
    assert data[1]["new_status"] == "Em Execução"


def test_email_sent_on_completion(mailoutbox):
    user, equip = _create_basic_objects()
    wo = work_order_service.create(
        {
            "equipment": equip,
            "priority": "Alta",
            "scheduled_date": date.today(),
            "created_by": user,
            "description": "Teste",
            "cost": 0,
        }
    )

    work_order_service.update_status(wo.id, "Em Execução", user)
    work_order_service.update_status(wo.id, "Concluída", user)

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == [user.email]
