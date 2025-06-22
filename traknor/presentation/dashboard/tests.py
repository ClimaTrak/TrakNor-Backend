from datetime import date, timedelta

import pytest
from django.urls import reverse

from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.work_orders.models import WorkOrder
from traknor.domain.constants import WorkOrderStatus

pytestmark = pytest.mark.django_db


def _create_user():
    return User.objects.create_user(
        email="user@example.com",
        password="pass",
        first_name="Test",
        last_name="User",
        role="technician",
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


def _create_work_order(user, equip, status=WorkOrderStatus.OPEN.value, days_ago=0):
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
    _create_work_order(user, eq1, WorkOrderStatus.OPEN.value, days_ago=10)
    _create_work_order(user, eq2, WorkOrderStatus.DONE.value, days_ago=40)

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


def test_kpi_endpoint(client):
    user = _create_user()
    equip = _create_equipment()
    _create_work_order(user, equip, WorkOrderStatus.DONE.value, days_ago=1)

    login_resp = client.post(
        reverse("accounts:login"),
        {"email": "user@example.com", "password": "pass"},
        content_type="application/json",
    )
    token = login_resp.json()["access"]

    resp = client.get(
        reverse("dashboard:kpis"),
        HTTP_AUTHORIZATION=f"Bearer {token}",
        data={"from": str(date.today() - timedelta(days=120)), "to": str(date.today())},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "open_workorders" in data


def test_mtbf_calculation(client):
    user = _create_user()
    equip = _create_equipment()
    for days in (100, 50, 10):
        wo = _create_work_order(user, equip, WorkOrderStatus.DONE.value, days_ago=days)
        wo.completed_date = date.today() - timedelta(days=days)
        wo.scheduled_date = wo.completed_date - timedelta(days=1)
        wo.save()

    login_resp = client.post(
        reverse("accounts:login"),
        {"email": "user@example.com", "password": "pass"},
        content_type="application/json",
    )
    token = login_resp.json()["access"]

    resp = client.get(reverse("dashboard:kpis"), HTTP_AUTHORIZATION=f"Bearer {token}")
    assert resp.status_code == 200
    data = resp.json()
    expected = (
        date.today() - timedelta(days=10) - date.today().replace(day=1)
    ).days * 24
    assert data["mtbf"] == float(expected)
