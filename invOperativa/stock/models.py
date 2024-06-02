from django.db import models

class Articulo(models.Model):
    fechaAltaArticulo = models.DateTimeField(auto_now_add=False) 
    fechaBajaArticulo = models.DateTimeField()
    





class Venta(models.Model):
    codVenta = models.IntegerField(null=True,
                                blank=True)
    cantVenta= models.IntegerField(null=True)
    fechaVenta= models.DateTimeField(null=True,
                                    auto_now_add=True)
    