from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.lista_pendientes, name = 'pendientes'),
    path('ventas/', ventas_por_mes, name = 'ventas'),
    path('crear-venta/', CrearVenta.as_view(), name='crear_venta'),
    path('crear-articulo/', CrearArticulo.as_view(), name='crear_articulo'),
    path('obtener-stock/', obtener_stock, name='obtener_stock'),
]

