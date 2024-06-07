from django.urls import path
from . import views
from .views import ventas_por_mes

urlpatterns = [
    path('', views.lista_pendientes, name = 'pendientes'),
    path('ventas/', ventas_por_mes, name = 'ventas'),
]

