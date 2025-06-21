from django.urls import path

from .views import PmocGenerateView

app_name = "pmoc"

urlpatterns = [
    path("generate/", PmocGenerateView.as_view(), name="generate"),
]
