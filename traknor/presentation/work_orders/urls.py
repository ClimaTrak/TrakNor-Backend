from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import WorkOrderViewSet

app_name = "work_orders"
router = DefaultRouter()
router.register(r"", WorkOrderViewSet, basename="workorder")

urlpatterns = [
    path("", include(router.urls)),
]
