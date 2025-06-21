from datetime import date

import pytest
from rest_framework.test import APIClient

from traknor.application.services import work_order_service
from traknor.domain.constants import WorkOrderStatus
from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.models.work_order_history import WorkOrderHistory

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
    assert wo.status == WorkOrderStatus.OPEN.value
    wo = work_order_service.update_status(wo.id, WorkOrderStatus.WAITING.value, user)
    assert wo.status == WorkOrderStatus.WAITING.value
    wo = work_order_service.update_status(
        wo.id, WorkOrderStatus.IN_PROGRESS.value, user
    )
    assert wo.status == WorkOrderStatus.IN_PROGRESS.value
    wo = work_order_service.update_status(wo.id, WorkOrderStatus.DONE.value, user)
    assert wo.status == WorkOrderStatus.DONE.value
    with pytest.raises(ValueError):
        work_order_service.update_status(wo.id, WorkOrderStatus.OPEN.value, user)


@pytest.mark.parametrize(
    "steps,new_status",
    [
        ([], WorkOrderStatus.IN_PROGRESS.value),
        ([], WorkOrderStatus.WAITING.value),
        ([WorkOrderStatus.WAITING.value], WorkOrderStatus.IN_PROGRESS.value),
        ([WorkOrderStatus.IN_PROGRESS.value], WorkOrderStatus.DONE.value),
    ],
)
def test_update_status_valid_transitions(steps, new_status):
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
    for status in steps:
        work_order_service.update_status(wo.id, status, user)
    wo = work_order_service.update_status(wo.id, new_status, user)
    assert wo.status == new_status


@pytest.mark.parametrize(
    "steps,new_status",
    [
        ([], WorkOrderStatus.DONE.value),
        ([WorkOrderStatus.IN_PROGRESS.value], WorkOrderStatus.WAITING.value),
        ([WorkOrderStatus.WAITING.value], WorkOrderStatus.DONE.value),
    ],
)
def test_update_status_invalid_transitions(steps, new_status):
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
    for status in steps:
        work_order_service.update_status(wo.id, status, user)
    with pytest.raises(ValueError):
        work_order_service.update_status(wo.id, new_status, user)


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
    work_order_service.update_status(wo.id, WorkOrderStatus.IN_PROGRESS.value, user)
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
    work_order_service.update_status(wo.id, WorkOrderStatus.IN_PROGRESS.value, user)
    work_order_service.update_status(wo.id, WorkOrderStatus.DONE.value, user)

    response = api_client.get(f"/api/work-orders/{wo.id}/history/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["new_status"] == WorkOrderStatus.DONE.value
    assert data[1]["new_status"] == WorkOrderStatus.IN_PROGRESS.value


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

    work_order_service.update_status(wo.id, WorkOrderStatus.IN_PROGRESS.value, user)
    work_order_service.update_status(wo.id, WorkOrderStatus.DONE.value, user)

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == [user.email]


def test_patch_status_persists(api_client):
    """PATCH update should change work order status in the database."""
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

    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/api/work-orders/{wo.id}/",
        {"status": WorkOrderStatus.IN_PROGRESS.value},
        format="json",
    )
    assert response.status_code == 200
    assert response.json()["status"] == WorkOrderStatus.IN_PROGRESS.value

    from traknor.infrastructure.work_orders.models import WorkOrder as WOModel

    assert WOModel.objects.get(id=wo.id).status == WorkOrderStatus.IN_PROGRESS.value
