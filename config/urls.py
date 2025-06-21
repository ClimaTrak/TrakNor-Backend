from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("traknor.presentation.accounts.urls")),
    path("api/equipment/", include("traknor.presentation.equipment.urls")),
    path("api/assets/", include("traknor.presentation.assets.urls")),
    path("api/work-orders/", include("traknor.presentation.work_orders.urls")),
    path("api/dashboard/", include("traknor.presentation.dashboard.urls")),
    path("api/pmoc/", include("traknor.presentation.pmoc.urls")),
    path("api/os/", include("traknor.presentation.os_api.urls")),
]
