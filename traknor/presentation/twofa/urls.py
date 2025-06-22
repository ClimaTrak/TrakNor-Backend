"""Routes for 2FA endpoints."""

from django.urls import path

from .views import (
    TwoFASetupView,
    TwoFAVerifyView,
    TwoFALoginStepView,
    TwoFADisableView,
)

app_name = "twofa"

urlpatterns = [
    path("api/2fa/setup/", TwoFASetupView.as_view(), name="2fa-setup"),
    path("api/2fa/verify/", TwoFAVerifyView.as_view(), name="2fa-verify"),
    path("api/2fa/", TwoFADisableView.as_view(), name="2fa-disable"),
    path("api/auth/2fa-token/", TwoFALoginStepView.as_view(), name="2fa-login-step"),
]
