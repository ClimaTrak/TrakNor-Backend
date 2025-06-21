import pytest
from django.urls import reverse
from datetime import date, timedelta

from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.work_orders.models import WorkOrder

pytestmark = pytest.mark.django_db


def _create_user():
    return User.objects.create_user(
        email="user@example.com",
        password="pass",
        first_name="Test",
        last_name="User",
        role="TECH",
    )


def _create_equipment(name="EQ", criticality="Média"):
    return EquipmentModel.objects.create(
        name=name,
        description="",
        type="Split",
        location="Loc",
        criticality=criticality,
        status="Operacional",
    )


def _create_work_order(user, equip, status="Aberta", days_ago=0):
    scheduled = date.today() - timedelta(days=days_ago)
    return WorkOrder.objects.create(
        equipment=equip,
        status=status,
        priority="Alta",
        scheduled_date=scheduled,
        created_by=user,
        description="D",
        cost=0,
    )


def test_dashboard_summary_counts(client):
    user = _create_user()
    eq1 = _create_equipment("EQ1", "Alta")
    eq2 = _create_equipment("EQ2", "Média")
    _create_work_order(user, eq1, "Aberta", days_ago=10)
    _create_work_order(user, eq2, "Concluída", days_ago=40)

    login_url = reverse("accounts:login")
    login_resp = client.post(
        login_url,
        {"email": "user@example.com", "password": "pass"},
        content_type="application/json",
    )
    token = login_resp.json()["access"]

    url = reverse("dashboard:summary")
    resp = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["total_equipment"] == 2
    assert data["open_work_orders"] == 1
    assert data["work_orders_last_30_days"] == 1
    assert data["critical_equipment"] == 1
