from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("traknor.presentation.accounts.urls")),
    path("api/equipment/", include("traknor.presentation.equipment.urls")),
    path("api/assets/", include("traknor.presentation.assets.urls")),
    path("api/work-orders/", include("traknor.presentation.work_orders.urls")),
    path("api/dashboard/", include("traknor.presentation.dashboard.urls")),
    path("api/pmoc/", include("traknor.presentation.pmoc.urls")),
    path("api/os/", include("traknor.presentation.os_api.urls")),
    path("api/reports/", include("traknor.presentation.reports.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema-json"),
    path("schema.yaml", SpectacularAPIView.as_view()),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc"),
]
