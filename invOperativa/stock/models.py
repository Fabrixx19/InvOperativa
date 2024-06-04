from django.db import models

class EstadoArticulo(models.Model):
    codEA = models.AutoField(primary_key=True)
    nombreEA = models.CharField(max_length=30,null=False)
    fechaHoraBajaEA = models.DateField(null=True, blank=True)


class Articulo(models.Model):
    codArticulo = models.AutoField(primary_key=True)
    fechaAltaArticulo = models.DateField(auto_now_add=True)
    fechaBajaArticulo = models.DateField(null=True, blank=True, max_length=30)
    nombreArticulo = models.CharField(max_length=30)
    stockArticulo = models.IntegerField()
    estado = models.ForeignKey(EstadoArticulo, on_delete=models.CASCADE, related_name='articulos')


class Demanda(models.Model):
    codDemanda = models.IntegerField(primary_key=True)
    valorDemanda = models.IntegerField()
    mesDemanda = models.DateField()

class Venta(models.Model):
    codVenta = models.AutoField(primary_key=True)
    cantVenta = models.IntegerField()
    fechaVenta = models.DateField(auto_now_add=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='ventas')

    #Una venta Tiene solo una demanda, pero una demanda muchas venttas
    demanda = models.ForeignKey(Demanda, on_delete=models.CASCADE, related_name='ventas')
    

class Prediccion_Demanda(models.Model):
    codPD = models.IntegerField(primary_key=True)
    cantPeriodos = models.IntegerField(null=False, blank=False)
    errorAceptable = models.IntegerField(null=False, blank=False)
    fechaBajaDemanda = models.DateField()
    resultadoPrediccion = models.IntegerField(null=False, blank=False)
    mesPrimerPeriodo = models.DateField()
    demandas = models.ManyToManyField(Demanda, related_name="predicciones")


class EstadoOrdenCompra(models.Model):
    codEC = models.AutoField(primary_key=True)
    nombreEC = models.CharField(null=False, blank=False, max_length=30)
    fechaHoraBajaEC = models.DateField(null=True, blank=True)


class Proveedor(models.Model):
    codProveedor = models.AutoField(primary_key=True)
    fechaBajaProveedor = models.DateField(null=True, blank=True)
    nombreProveedor = models.CharField(null=False, blank=False, max_length=30)
    

class OrdenDeCompra(models.Model):
    codODC = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    estado = models.ForeignKey(EstadoOrdenCompra, on_delete=models.CASCADE, related_name='ordenes')
    prediccion = models.OneToOneField(Prediccion_Demanda, on_delete=models.CASCADE)
    