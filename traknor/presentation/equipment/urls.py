from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EquipmentViewSet

router = DefaultRouter()
router.register(r'', EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('', include(router.urls)),
]
