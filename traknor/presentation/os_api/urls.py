from django.urls import path

from .views import OsListView

app_name = "os_api"

urlpatterns = [
    path("", OsListView.as_view(), name="list"),
]
