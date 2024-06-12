from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View, ListView
from django.urls import reverse_lazy
from metodos_demanda import *

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


class ModificarArticulo(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'modificar_articulo.html'
    success_url = reverse_lazy('lista_articulos')


class DarDeBajaArticulo(View):
    success_url = reverse_lazy('lista_articulos')
    
    def post(self, request, pk):
        articulo = get_object_or_404(Articulo, pk=pk)
        articulo.fechaBajaArticulo = datetime.now()  # Marca la fecha de baja como la fecha actual
        articulo.save()
        return redirect(self.success_url)
    def get(self, request, pk):  # Opcional para debugging
        return redirect(self.success_url)


class ListaArticulos(ListView):
    model = Articulo
    template_name = 'lista_articulos.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        return Articulo.objects.filter(fechaBajaArticulo__isnull=True)   


def ver_demandas_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    demandas = articulo.demandas.exclude(demandaPredecida=0, demandaReal=0).order_by('-anioDemanda', '-mesDemanda')
    return render(request, 'demandas_articulos.html', {'articulo': articulo, 'demandas': demandas})


def ver_ventas_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    ventas = articulo.ventas.order_by('-fechaVenta')
    return render(request, 'ventas_articulo.html', {'articulo': articulo, 'ventas': ventas})

class PredecirDemanda(CreateView):
    model = Prediccion_Demanda
    form_class = PrediccionDemandaForm
    template_name = 'crear_demanda.html'
    success_url = reverse_lazy('pendientes')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        prediccion = self.object  # El artículo recién creado

        # Crear demandas automáticas para los últimos tres años y el año actual
        demanda_exponencial = self.metodo_exponen(prediccion)
        demanda_ponderado = self.metodo_ponderado(prediccion)
        
        
        
        return response
    
    def metodo_exponen(self, prediccion):
        mes = prediccion.mesPrimerPeriodo
        anio = prediccion.anioPrimerPeriodo
        if mes == 1:
            mes = 13
            anio -= 1
        
        cofSua = prediccion.coeficienteSuavizacion
        demandaAnterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-1)
        demanda_real_anterior = demandaAnterior.demandaReal
        demanda_predecida_anterior = demandaAnterior.demandaPredecida
        if demanda_predecida_anterior == 0:
            if mes == 2:
                mes = 14
                anio -= 1
                
            demanda_predecida_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-2).demandaReal
        
        demanda_predecida_exponencial = promedioExponencia(demanda_predecida_anterior, demanda_real_anterior, cofSua)
        return demanda_predecida_exponencial    
        
    def metodo_ponderado(self, prediccion):
        n = prediccion.cantPeriodos - 1
        mes = prediccion.mesPrimerPeriodo
        anio = prediccion.anioPrimerPeriodo
        if mes == 1 :
            mes = 13,
            anio -= 1
             
        demanda = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-1)
        demandas = []
        demandas.append(demanda.demandaReal)
        
        for i in range(1,n):
            if mes <= i:
                mes = 13
                anio -= 1
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-i)
            demandas.append(prediccion_anterior.demandaReal)
        
        demanda_ponde = promedio_movil_ponderado(demandas)
        return demanda_ponde
        

        
