from django.db import models

class EstadoArticulo(models.Model):
    codEA = models.AutoField(primary_key=True)
    nombreEA = models.CharField(max_length=30,null=False)
    fechaHoraBajaEA = models.DateField(null=True, blank=True)


class ModeloInventario(models.Model):
    codMI = models.AutoField(primary_key=True)
    nombreMI = models.CharField(max_length=30,null=False)


class Proveedor(models.Model):
    codProveedor = models.AutoField(primary_key=True)
    fechaBajaProveedor = models.DateField(null=True, blank=True)
    nombreProveedor = models.CharField(null=False, blank=False, max_length=30)
    diasDeDemora = models.IntegerField(null=False, blank=False)
    precioXunidad = models.FloatField(null=False, blank=False)
    costo_pedido = models.FloatField(null=False, blank=False)   


class Articulo(models.Model):
    codArticulo = models.AutoField(primary_key=True)
    fechaAltaArticulo = models.DateField(auto_now_add=True)
    fechaBajaArticulo = models.DateField(null=True, blank=True)
    nombreArticulo = models.CharField(max_length=30)
    stockArticulo = models.IntegerField()
    puntoPedido = models.IntegerField(default=0)
    stockSeguridad = models.IntegerField(default=0)
    loteOptimo = models.IntegerField(default=0)
    cgi = models.FloatField(default=0)
    cantidasIntervaloFijo = models.IntegerField(default=0)
    estado = models.ForeignKey(EstadoArticulo, on_delete=models.CASCADE, related_name='articulos')
    modeloInventario = models.ForeignKey(ModeloInventario, on_delete=models.CASCADE, related_name="articulos")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='articulos', null=True)
    metodo = models.TextField(default="", null=True, blank=True)
    prediccion_predeterminada = models.ForeignKey('Prediccion_Demanda', on_delete=models.SET_NULL, related_name='articulos_predeterminados', null=True, blank=True)


class Demanda(models.Model):
    codDemanda = models.AutoField(primary_key=True)
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
    codME = models.AutoField(primary_key=True)
    nombreME = models.CharField(null=False, blank=False, max_length=30)
    fechaBajaME = models.DateField(null=True, blank=True)    

    
class Prediccion_Demanda(models.Model):
    codPD = models.AutoField(primary_key=True)
    cantPeriodos = models.IntegerField(null=True) #ingresa
    coeficienteSuavizacion = models.FloatField(null=True) #ingresa
    mesPrediccion = models.IntegerField()    #ingresa
    anioPrediccion = models.IntegerField()   #ingresa
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='predicciones')
    metodoError = models.ForeignKey(MetodoError, on_delete=models.CASCADE, related_name='predicciones', null=True) #Ingresar
    

class EstadoOrdenCompra(models.Model):
    codEC = models.AutoField(primary_key=True)
    nombreEC = models.CharField(null=False, blank=False, max_length=30)
    fechaHoraBajaEC = models.DateField(null=True, blank=True)


class OrdenDeCompra(models.Model):
    codODC = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    estado = models.ForeignKey(EstadoOrdenCompra, on_delete=models.CASCADE, related_name='ordenDeCompra')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='ordenDeCompra')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='ordenDeCompra')
    fechaOrden = models.DateField(auto_now_add=True)
    diasDemoraOrden = models.IntegerField()
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Solo establece diasDemoraOrden cuando se crea el objeto
            self.diasDemoraOrden = self.proveedor.diasDeDemora
            estado_pendiente = EstadoOrdenCompra.objects.get(nombreEC='Pendiente')
            self.estado = estado_pendiente
        super().save(*args, **kwargs)
