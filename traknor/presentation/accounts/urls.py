"""URL routes for authentication endpoints."""

from django.urls import path

from .views import LoginView, RefreshView, RegisterView

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
]
