from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

#Agregado por mi para ver si anda
from .models import Venta
from .forms import *
from django.db.models import Sum
from datetime import datetime

# Create your views here.

def lista_pendientes(pedido):
    return HttpResponse('Hola ando')


# Esta vista es para procesar la solicitud del ususario
def ventas_por_mes(request):
    form = DatosPrediccionFrom(request.GET or None)
    total_cant_ventas=0

    if form.is_valid():
        mes = int(form.cleaned_data['mes'])
        anio = int(form.cleaned_data['anio'])

        #Obtener el primer y ultimo dia del mes
        primer_dia_mes = datetime(year=anio ,month=mes, day=1)
        if mes == 12:
                ultimo_dia_mes = datetime(year=anio + 1, month=1, day=1)
        else:
                ultimo_dia_mes = datetime(year=anio, month=mes + 1, day=1)
        
        #Filtrar las ventas por el rango de fechas del mes seleccionado
        ventas = Venta.objects.filter(fechaVenta__gte=primer_dia_mes, fechaVenta__lt=ultimo_dia_mes)
        
        total_cant_ventas = 0
        for v in ventas:
            total_cant_ventas += v.cantVenta
        

    return render(request, 'ventas_por_mes.html',{
        'form':form,
        'total_cant_ventas': total_cant_ventas,
    })


class CrearVenta(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'crear_venta.html'  
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        mes, año = self.object.fechaVenta.month, self.object.fechaVenta.year
        articulo = self.object.articulo

        if articulo.stockArticulo < self.object.cantVenta:
            form.add_error('cantVenta', 'Stock insuficiente para realizar la venta')
            return self.form_invalid(form)

        # Buscar la demanda existente para el artículo, mes y año especificados
        demanda_existente = Demanda.objects.get(
            mesDemanda=mes,
            anioDemanda=año,
            articulo=articulo
        )

        # Actualizar la demanda real
        demanda_existente.demandaReal += self.object.cantVenta
        demanda_existente.save()
        self.object.demanda = demanda_existente

        # Reducir el stock del artículo
        articulo.stockArticulo -= self.object.cantVenta
        articulo.save()

        # Guardar la venta con la demanda asociada
        self.object.save()
        return super().form_valid(form)

class CrearArticulo(CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'crear_articulo.html'
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        response = super().form_valid(form)
        articulo = self.object  # El artículo recién creado

        # Crear demandas automáticas para los últimos tres años y el año actual
        self.crear_demandas_automaticas(articulo)
        
        return response

    def crear_demandas_automaticas(self, articulo):
        current_year = datetime.now().year
        years = [current_year - 3, current_year - 2, current_year - 1, current_year]

        for year in years:
            for month in range(1, 12 + 1):
                Demanda.objects.get_or_create(
                    mesDemanda=month,
                    anioDemanda=year,
                    articulo=articulo,
                    defaults={'demandaReal': 0, 'demandaPredecida': 0}
                )

def obtener_stock(request):
    articulo_id = request.GET.get('articulo_id')
    if articulo_id:
        try:
            articulo = Articulo.objects.get(pk=articulo_id)
            stock = articulo.stockArticulo
        except Articulo.DoesNotExist:
            stock = 'Artículo no encontrado'
    else:
        stock = 'Selecciona un artículo'

    return JsonResponse({'stock': stock})   
