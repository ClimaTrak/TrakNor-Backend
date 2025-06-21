from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EquipmentViewSet
from .import_view import EquipmentImportView

app_name = "equipment"

router = DefaultRouter()
router.register(r'', EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('', include(router.urls)),
    path('import/', EquipmentImportView.as_view(), name='equipment-import'),
]
