"""API views for two-factor authentication stub."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from traknor.application.services import twofa_service


class TwoFASetupView(APIView):
    """Begin 2FA setup returning QR code and otpauth URL."""

    permission_classes = [IsAuthenticated]

    def post(self, request):  # pragma: no cover - thin wrapper
        url, qr = twofa_service.setup_totp(request.user)
        return Response({"otpauth_url": url, "qr": qr})


class TwoFAVerifyView(APIView):
    """Verify initial 2FA token and activate device."""

    permission_classes = [IsAuthenticated]

    def post(self, request):  # pragma: no cover - thin wrapper
        token = request.data.get("token", "")
        if twofa_service.confirm_totp(request.user, token):
            return Response({"detail": "2FA enabled"})
        return Response({"detail": "Invalid token"}, status=400)


class TwoFALoginStepView(APIView):
    """Exchange temp token and OTP for real JWT."""

    def post(self, request):  # pragma: no cover - thin wrapper
        temp_token = request.data.get("temp_token", "")
        token = request.data.get("token", "")
        user = twofa_service.verify_temp_token(temp_token)
        if not user or not twofa_service.check_token(user, token):
            return Response({"detail": "Invalid token"}, status=400)
        data = TokenObtainPairSerializer.get_token(user)
        return Response({"access": str(data.access_token), "refresh": str(data)})


class TwoFADisableView(APIView):
    """Disable 2FA for authenticated user."""

    permission_classes = [IsAuthenticated]

    def delete(self, request):  # pragma: no cover - thin wrapper
        twofa_service.disable_2fa(request.user)
        return Response(status=204)
