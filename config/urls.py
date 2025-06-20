from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("traknor.presentation.accounts.urls")),
    path("equipment/", include("traknor.presentation.equipment.urls")),
    path("work-orders/", include("traknor.presentation.work_orders.urls")),
]
