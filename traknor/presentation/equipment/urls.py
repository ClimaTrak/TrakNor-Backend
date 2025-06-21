from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EquipmentViewSet
from .import_view import EquipmentImportView

# Do not namespace these routes so reverse('equipment-list') works without a
# prefix. Tests expect the un-namespaced route name.

router = DefaultRouter()
router.register(r'', EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('', include(router.urls)),
    path('import/', EquipmentImportView.as_view(), name='equipment-import'),
]
