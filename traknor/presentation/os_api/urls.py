from django.urls import path

from .views import OsListView, OsExecuteView, OpenOrdersListView

app_name = "os_api"

urlpatterns = [
    path("", OsListView.as_view(), name="list"),
    path("open/", OpenOrdersListView.as_view(), name="open"),
    path("<int:pk>/execute/", OsExecuteView.as_view(), name="execute"),
]
