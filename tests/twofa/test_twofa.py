import pytest
from django.urls import reverse
from django.test.utils import override_settings
from importlib import reload
from django.urls import clear_url_caches
import config.urls as urls
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.oath import totp

from traknor.infrastructure.accounts.user import User

pytestmark = pytest.mark.django_db


@override_settings(ENABLE_2FA=True)
def test_setup_and_verify(client):
    reload(urls)
    clear_url_caches()
    user = User.objects.create_user(
        email="u@example.com",
        password="pass",
        first_name="U",
        last_name="User",
        role="technician",
    )
    login_resp = client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "pass"},
        content_type="application/json",
    )
    jwt_token = login_resp.json()["access"]
    resp = client.post("/api/2fa/setup/", HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
    assert resp.status_code == 200
    device = TOTPDevice.objects.get(user=user)
    otp_token = totp(device.bin_key, step=device.step, t0=device.t0)
    verify = client.post(
        "/api/2fa/verify/",
        {"token": otp_token},
        HTTP_AUTHORIZATION=f"Bearer {jwt_token}",
    )
    user.refresh_from_db()
    assert verify.status_code == 200
    assert user.is_2fa_enabled


@override_settings(ENABLE_2FA=True)
def test_login_two_steps(client):
    reload(urls)
    clear_url_caches()
    user = User.objects.create_user(
        email="2fa@example.com",
        password="pass",
        first_name="Two",
        last_name="FA",
        role="technician",
        is_2fa_enabled=True,
    )
    device = TOTPDevice.objects.create(user=user, name="default", confirmed=True)
    login = client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "pass"},
        content_type="application/json",
    )
    assert login.status_code == 202
    temp = login.json()["temp_token"]
    otp_token = totp(device.bin_key, step=device.step, t0=device.t0)
    step = client.post(
        "/api/auth/2fa-token/",
        {"temp_token": temp, "token": otp_token},
        content_type="application/json",
    )
    assert step.status_code == 200
    assert "access" in step.json()


@override_settings(ENABLE_2FA=False)
def test_flag_disabled_returns_404(client):
    reload(urls)
    clear_url_caches()
    user = User.objects.create_user(
        email="no2fa@example.com",
        password="pass",
        first_name="N",
        last_name="User",
        role="technician",
    )
    client.force_login(user)
    resp = client.post("/api/2fa/setup/")
    assert resp.status_code == 404
