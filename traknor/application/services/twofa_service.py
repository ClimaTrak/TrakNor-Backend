from __future__ import annotations

"""Service utilities for two-factor authentication."""

import base64
import io
import logging
from typing import Tuple, Optional

from django.contrib.auth import get_user_model
from django.core import signing
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode

logger = logging.getLogger(__name__)
UserModel = get_user_model()


def generate_temp_token(user: UserModel) -> str:
    """Return a short-lived signed token for 2FA login step."""
    return signing.dumps({"uid": user.pk}, salt="2fa-temp")


def verify_temp_token(token: str) -> Optional[UserModel]:
    """Return user if temp token is valid."""
    try:
        data = signing.loads(token, salt="2fa-temp", max_age=300)
    except signing.BadSignature:
        return None
    return UserModel.objects.filter(pk=data.get("uid")).first()


def setup_totp(user: UserModel) -> Tuple[str, str]:
    """Create or reset a TOTP device and return otpauth url and QR base64."""
    device, _ = TOTPDevice.objects.get_or_create(user=user, name="default")
    device.confirmed = False
    device.save()
    qr = qrcode.make(device.config_url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()
    return device.config_url, qr_b64


def confirm_totp(user: UserModel, token: str) -> bool:
    """Validate token and activate device."""
    try:
        device = user.totpdevice_set.get(name="default")
    except TOTPDevice.DoesNotExist:
        return False
    if device.verify_token(token):
        device.confirmed = True
        device.save()
        user.is_2fa_enabled = True
        user.save(update_fields=["is_2fa_enabled"])
        return True
    return False


def check_token(user: UserModel, token: str) -> bool:
    """Verify token for confirmed device."""
    try:
        device = user.totpdevice_set.get(name="default", confirmed=True)
    except TOTPDevice.DoesNotExist:
        return False
    return device.verify_token(token)


def disable_2fa(user: UserModel) -> None:
    """Remove all devices and disable flag."""
    user.totpdevice_set.all().delete()
    user.is_2fa_enabled = False
    user.save(update_fields=["is_2fa_enabled"])


def send_sms_stub(phone: str, message: str) -> None:
    """Log SMS message for stub implementation."""
    logger.info("SMS to %s :: %s", phone, message)
