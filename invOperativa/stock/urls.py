from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.lista_pendientes, name = 'pendientes'),
    path('ventas/', ventas_por_mes, name = 'ventas'),
    path('crear-venta/', CrearVenta.as_view(), name='crear_venta'),
    path('articulos/crear/', CrearArticulo.as_view(), name='crear_articulo'),
    path('obtener-stock/', obtener_stock, name='obtener_stock'),
    path('articulos/modificar/<int:pk>/', ModificarArticulo.as_view(), name='modificar_articulo'),
    path('articulos/baja/<int:pk>/', DarDeBajaArticulo.as_view(), name='baja_articulo'),
    path('articulos/', ListaArticulos.as_view(), name='lista_articulos'),
    path('articulos/<int:articulo_id>/demandas/', views.ver_demandas_articulo, name='demandas_articulo'),
    path('articulos/<int:articulo_id>/ventas/', views.ver_ventas_articulo, name='ventas_articulo'),

]

