from django.urls import path
from . import views

app_name = "work_orders"
urlpatterns = [
    path('', views.index, name='index'),
]


