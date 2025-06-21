import pytest
from rest_framework.test import APIRequestFactory

from traknor.infrastructure.accounts.user import User
from traknor.presentation.permissions import IsAdmin, IsManager, IsTechnician

pytestmark = pytest.mark.django_db


def test_is_admin():
    factory = APIRequestFactory()
    user = User.objects.create_user(
        email="admin@example.com",
        password="pass",
        first_name="Admin",
        last_name="User",
        role="admin",
    )
    request = factory.get("/any")
    request.user = user
    assert IsAdmin().has_permission(request, None)

    request.user.role = "technician"
    assert not IsAdmin().has_permission(request, None)


def test_other_roles():
    factory = APIRequestFactory()
    user = User.objects.create_user(
        email="mgr@example.com",
        password="pass",
        first_name="Mgr",
        last_name="User",
        role="manager",
    )
    request = factory.get("/any")
    request.user = user
    assert IsManager().has_permission(request, None)
    assert not IsTechnician().has_permission(request, None)

    request.user.role = "technician"
    assert IsTechnician().has_permission(request, None)
