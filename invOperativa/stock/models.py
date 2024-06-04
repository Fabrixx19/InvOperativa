from django.db import models

class Articulo(models.Model):
    codArticulo = models.AutoField(primary_key=True)
    fechaAltaArticulo = models.DateTimeField(auto_now_add=True)
    fechaBajaArticulo = models.DateTimeField(null=True, blank=True)
    nombreArticulo = models.CharField(max_length=30)
    stockArticulo = models.IntegerField()
    

class Venta(models.Model):
    codVenta = models.AutoField(primary_key=True)
    cantVenta = models.IntegerField(null=True, blank=True)
    fechaVenta = models.DateTimeField(auto_now_add=True)
    articulo = models.OneToOneField(Articulo, on_delete=models.CASCADE)
