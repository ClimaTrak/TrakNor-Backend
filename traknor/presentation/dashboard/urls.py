from django.urls import path

from .views import DashboardSummaryView, KPIView

app_name = "dashboard"

urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="summary"),
    path("kpis/", KPIView.as_view(), name="kpis"),
]
