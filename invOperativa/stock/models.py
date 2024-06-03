from django.db import models

class Articulo(models.Model):
    codArticulo = models.AutoField(primary_key=True)
    fechaAltaArticulo = models.DateTimeField(auto_now_add=False) 
    fechaBajaArticulo = models.DateTimeField()
    nombreArticulo = models.TextField(max_length=30)
    stockArticulo = models.IntegerField()
    





class Venta(models.Model):
    codVenta = models.AutoField(primary_key=True)
    cantVenta= models.IntegerField(null=True)
    fechaVenta= models.DateTimeField(null=True,
                                    auto_now_add=True)
    articulo= models.OneToOneField(Articulo, on_delete=models.CASCADE)
    