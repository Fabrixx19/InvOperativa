from django.db import models

class EstadoArticulo(models.Model):
    codEA = models.AutoField(primary_key=True)
    nombreEA = models.CharField(max_length=30,null=False)
    fechaHoraBajaEA = models.DateField(null=True, blank=True)

class ModeloInventario(models.Model):
    codMI = models.AutoField(primary_key=True)
    nombreMI = models.CharField(max_length=30,null=False)
    

class Articulo(models.Model):
    codArticulo = models.AutoField(primary_key=True)
    fechaAltaArticulo = models.DateField(auto_now_add=True)
    fechaBajaArticulo = models.DateField(null=True, blank=True, max_length=30)
    nombreArticulo = models.CharField(max_length=30)
    stockArticulo = models.IntegerField()
    puntoPedido = models.IntegerField()
    stockSeguridad = models.IntegerField()
    loteOptimo = models.IntegerField()
    estado = models.ForeignKey(EstadoArticulo, on_delete=models.CASCADE, related_name='articulos')
    modeloInventario = models.ForeignKey(ModeloInventario, on_delete=models.CASCADE, related_name="articulos")

class Proveedor(models.Model):
    codProveedor = models.AutoField(primary_key=True)
    fechaBajaProveedor = models.DateField(null=True, blank=True)
    nombreProveedor = models.CharField(null=False, blank=False, max_length=30)
    tiempoDeDemora = models.DateField(null=False, blank=False)
    precioXunidad = models.FloatField(null=False, blank=False)
    costo_pedido = models.FloatField(null=False, blank=False)
    articulo = models.OneToOneField(Articulo, on_delete=models.CASCADE)


class Demanda(models.Model):
    codDemanda = models.IntegerField(primary_key=True)
    demandaReal = models.IntegerField(default=0)
    demandaPredecida = models.IntegerField(default=0)
    mesDemanda = models.IntegerField()
    anioDemanda = models.IntegerField()
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='demandas')

class Venta(models.Model):
    codVenta = models.AutoField(primary_key=True)
    cantVenta = models.IntegerField()
    fechaVenta = models.DateField()
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='ventas')
    #Una venta Tiene solo una demanda, pero una demanda muchas venttas
    demanda = models.ForeignKey(Demanda, on_delete=models.CASCADE, related_name='ventas')

class MetodoError(models.Model):
    codME = models.IntegerField(primary_key=True)
    nombreME = models.CharField(null=False, blank=False, max_length=30)
    fechaBajaME = models.DateField()    
    
class Prediccion_Demanda(models.Model):
    codPD = models.IntegerField(primary_key=True)
    cantPeriodos = models.IntegerField(null=False, blank=False) #ingresa
    coeficienteSuavizacion = models.FloatField(null=False, blank=False) #ingresa
    errorAceptable = models.FloatField(null=False, blank=False) #ingresa
    mesPrimerPeriodo = models.IntegerField()    #ingresa
    anioPrimerPeriodo = models.IntegerField()   #ingresa
    demandas = models.ManyToManyField(Demanda, related_name="predicciones")
    metodoError = models.ForeignKey(MetodoError, on_delete=models.CASCADE, related_name='predicciones') #Ingresar
    

class EstadoOrdenCompra(models.Model):
    codEC = models.AutoField(primary_key=True)
    nombreEC = models.CharField(null=False, blank=False, max_length=30)
    fechaHoraBajaEC = models.DateField(null=True, blank=True)

class OrdenDeCompra(models.Model):
    codODC = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    estado = models.ForeignKey(EstadoOrdenCompra, on_delete=models.CASCADE, related_name='ordenDeCompra')
    prediccion = models.OneToOneField(Prediccion_Demanda, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='ordenDeCompra')
