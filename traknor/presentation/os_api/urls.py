from django.urls import path

from .views import OpenOrdersListView, OsExecuteView, OsListView

app_name = "os_api"

urlpatterns = [
    path("", OsListView.as_view(), name="list"),
    path("open/", OpenOrdersListView.as_view(), name="open"),
    path("<int:id>/execute/", OsExecuteView.as_view(), name="execute"),
]
