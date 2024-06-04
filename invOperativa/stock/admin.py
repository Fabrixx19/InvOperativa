from django.contrib import admin
from .models import Articulo, Venta, OrdenDeCompra, EstadoArticulo, EstadoOrdenCompra, Proveedor, Prediccion_Demanda, Demanda
# Register your models here.

admin.site.register(Articulo)
admin.site.register(Venta)
admin.site.register(OrdenDeCompra)
admin.site.register(Proveedor)
admin.site.register(Demanda)
admin.site.register(Prediccion_Demanda)
admin.site.register(EstadoOrdenCompra)
admin.site.register(EstadoArticulo)