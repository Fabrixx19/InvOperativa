from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.inicio, name = 'inicio'),
    path('ventas/', ventas_por_mes, name = 'ventas'),
    path('crear-venta/', CrearVenta.as_view(), name='crear_venta'),
    path('articulos/crear/', CrearArticulo.as_view(), name='crear_articulo'),
    path('obtener-stock/', obtener_stock, name='obtener_stock'),
    path('articulos/modificar/<int:pk>/', ModificarArticulo.as_view(), name='modificar_articulo'),
    path('articulos/baja/<int:pk>/', DarDeBajaArticulo.as_view(), name='baja_articulo'),
    path('articulos/', ListaArticulos.as_view(), name='lista_articulos'),
    path('articulos/<int:articulo_id>/demandas/', views.ver_demandas_articulo, name='demandas_articulo'),
    path('articulos/<int:articulo_id>/ventas/', views.ver_ventas_articulo, name='ventas_articulo'),
    path('predecir/', PredecirDemanda.as_view(), name='predecir_demanda'),
    path('resultados/', ResultadosDemanda.as_view(), name='resultados_demanda'),
    path('articulo/<int:pk>/asignar_proveedor/', AsignarProveedorView.as_view(), name='asignar_proveedor'),
    path('elegirMPrediccion', views.elegirMPrediccion, name = 'elegirMPrediccion'),
    path('crear_orden/', CrearOrdenDeCompraView.as_view(), name='crear_orden_de_compra'),
    path('ordenes/', ListarOrdenesDeCompraView.as_view(), name='listar_ordenes_de_compra'),
    path('verificar_entregas/', VerificarEntregasView.as_view(), name='verificar_entregas'),
    path('predecir_ponderado/', PrediccionPonderadoView.as_view(), name='predecir_ponderado'),
    path('predecir_exponencial/', PrediccionExponencialView.as_view(), name='predecir_exponencial'),
    path('predecir_regresion/', PrediccionRegresionView.as_view(), name='predecir_regresion'),
    path('predecir_estacional/', PrediccionEstacionalView.as_view(), name='predecir_estacional'),
    path('resultado_demanda/<int:resultado>/<str:metodo>/', resultado_demanda_view, name='resultado_demanda'),
    path('lista_articulos_faltantes/', ListaArticulosFaltantes.as_view(), name='lista_articulos_faltantes'),
    path('lista_articulos_reponer/', ListaArticulosReponer.as_view(), name='lista_articulos_reponer'),



]

