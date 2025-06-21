from datetime import date

import pytest
from django.urls import reverse

from traknor.infrastructure.accounts.user import User
from traknor.infrastructure.equipment.models import EquipmentModel
from traknor.infrastructure.work_orders.models import WorkOrder

pytestmark = pytest.mark.django_db


def _create_user():
    return User.objects.create_user(
        email="tech@example.com",
        password="pass",
        first_name="Tech",
        last_name="User",
        role="TECH",
    )


def _create_equipment():
    return EquipmentModel.objects.create(
        name="EQ1",
        description="",
        type="Split",
        location="Room",
        criticality="Média",
        status="Operacional",
    )


def _create_work_order(user, equip, sched_date):
    return WorkOrder.objects.create(
        equipment=equip,
        status="Aberta",
        priority="Alta",
        scheduled_date=sched_date,
        created_by=user,
        description="Test",
        cost=0,
    )


def _auth_headers(client, email="tech@example.com", password="pass"):
    login_url = reverse("accounts:login")
    resp = client.post(
        login_url,
        {"email": email, "password": password},
        content_type="application/json",
    )
    token = resp.json()["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


def test_list_today_os(client):
    user = _create_user()
    equip = _create_equipment()
    _create_work_order(user, equip, date.today())
    _create_work_order(user, equip, date.today())

    headers = _auth_headers(client)
    url = reverse("os_api:list") + "?assignee=me&date=today"
    resp = client.get(url, **headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_invalid_params(client):
    user = _create_user()
    equip = _create_equipment()
    _create_work_order(user, equip, date.today())

    headers = _auth_headers(client)
    url = reverse("os_api:list") + "?assignee=me&date=bad"
    resp = client.get(url, **headers)
    assert resp.status_code == 400


def test_execute_success(client):
    user = _create_user()
    equip = _create_equipment()
    wo = _create_work_order(user, equip, date.today())
    wo.status = "Em Execução"
    wo.save()

    headers = _auth_headers(client)
    url = reverse("os_api:execute", args=[wo.id])
    resp = client.patch(url, **headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "Concluída"


def test_execute_forbidden(client):
    _create_user()
    other = User.objects.create_user(
        email="other@example.com",
        password="pass",
        first_name="O",
        last_name="U",
        role="TECH",
    )
    equip = _create_equipment()
    wo = _create_work_order(other, equip, date.today())
    wo.status = "Em Execução"
    wo.save()

    headers = _auth_headers(client)
    url = reverse("os_api:execute", args=[wo.id])
    resp = client.patch(url, **headers)
    assert resp.status_code == 403


def test_open_orders_list(client):
    user = _create_user()
    equip = _create_equipment()
    _create_work_order(user, equip, date.today())
    _create_work_order(user, equip, date.today())

    headers = _auth_headers(client)
    url = reverse("os_api:open")
    resp = client.get(url + "?limit=1&offset=0", **headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
