from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EquipmentViewSet

app_name = "equipment"

router = DefaultRouter()
router.register(r'', EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('', include(router.urls)),
]
