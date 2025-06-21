import pytest
from datetime import date

from traknor.application.services import work_order_state_machine
from traknor.domain.constants import WorkOrderStatus
from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.work_orders.models import WorkOrder

pytestmark = pytest.mark.django_db


def _setup():
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
    wo = WorkOrder.objects.create(
        equipment=equip,
        priority="Alta",
        scheduled_date=date.today(),
        created_by=user,
        description="Test",
        cost=0,
    )
    return user, wo


def test_valid_transition():
    user, wo = _setup()
    work_order_state_machine.change_status(
        wo, WorkOrderStatus.IN_PROGRESS, user, wo.revision
    )
    assert wo.status == WorkOrderStatus.IN_PROGRESS
    assert wo.revision == 1


def test_invalid_transition():
    user, wo = _setup()
    with pytest.raises(Exception):
        work_order_state_machine.change_status(
            wo, WorkOrderStatus.DONE, user, wo.revision
        )


def test_concurrency_error():
    user, wo = _setup()
    with pytest.raises(Exception):
        work_order_state_machine.change_status(
            wo, WorkOrderStatus.IN_PROGRESS, user, wo.revision + 1
        )


def test_soft_delete():
    user, wo = _setup()[0:2]
    wo.delete()
    assert wo.deleted_at is not None
    assert WorkOrder.objects.filter(id=wo.id).count() == 0
    assert WorkOrder.objects.all_with_deleted().filter(id=wo.id).exists()
