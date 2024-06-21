from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View, ListView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
import math


from math import ceil, sqrt
import statistics

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
    template_name = 'crear_prediccion.html'
    success_url = reverse_lazy('pendientes')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        prediccion = self.object  
        
        cant_periodos = form.cleaned_data['cantPeriodos']
        mes_primer_periodo = form.cleaned_data['mesPrimerPeriodo']
        anio_primer_periodo = form.cleaned_data['anioPrimerPeriodo']
        error_aceptable = form.cleaned_data['errorAceptable']
        
        # Obtener pesos del formulario
        pesos = list(map(float, self.request.POST['pesos'].split(',')))
        print(pesos)
        
        if len(pesos) != cant_periodos:
            form.add_error('pesos', f"Debe ingresar exactamente {cant_periodos} pesos.")
            return self.form_invalid(form)

        
        demanda_exponencial = self.metodo_exponen(prediccion)
        demanda_ponderado = self.metodo_ponderado(prediccion, pesos)
        demanda_regresion = self.metodo_regresion(prediccion)
        demanda_estacional = self.metodo_estacional(prediccion, demanda_regresion)
        
        metodo_error = form.cleaned_data['metodoError']
        if metodo_error.nombreME == "Cuadrado Medio":
            error_exp = self.metodo_cuadrado(prediccion, demanda_exponencial)
            error_ponderado = self.metodo_cuadrado(prediccion, demanda_ponderado)
            error_regresion = self.metodo_cuadrado(prediccion, demanda_regresion)
            error_estacional = self.metodo_cuadrado(prediccion, demanda_estacional)
        else:
            error_exp = self.metodo_porcentual(prediccion, demanda_exponencial)
            error_ponderado = self.metodo_porcentual(prediccion, demanda_ponderado)
            error_regresion = self.metodo_porcentual(prediccion, demanda_regresion)
            error_estacional = self.metodo_porcentual(prediccion, demanda_estacional)
        
        # Almacenar los resultados en la sesión
        self.request.session['resultados_prediccion'] = {
            'demanda_exponencial': demanda_exponencial,
            'demanda_ponderado': demanda_ponderado,
            'demanda_regresion': demanda_regresion,
            'demanda_estacional': demanda_estacional,
            'error_exp': error_exp,
            'error_ponderado': error_ponderado,
            'error_regresion': error_regresion,
            'error_estacional': error_estacional,
            'mes_primer_periodo': mes_primer_periodo,
            'anio_primer_periodo': anio_primer_periodo,
            'error_aceptable': error_aceptable
        }
        
        # Redirigir a la vista de resultados
        return redirect('resultados_demanda')
    
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
        
    def metodo_ponderado(self, prediccion, pesos):
        n = prediccion.cantPeriodos
        mes = prediccion.mesPrimerPeriodo
        anio = prediccion.anioPrimerPeriodo
        
        demandas = []
        for i in range(1,n+1):
            if mes <= i:
                mes = 13
                anio -= 1
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-i)
            demandas.append(prediccion_anterior.demandaReal)
        print(f"las demandas que mande son {demandas}")
        
        demanda_ponde = promedio_movil_ponderado(demandas, pesos)
        return demanda_ponde
        
    def metodo_regresion(self, prediccion):
        
        n = prediccion.cantPeriodos
        mes = prediccion.mesPrimerPeriodo
        anio = prediccion.anioPrimerPeriodo
        
        demandas = []
        for i in range(1,n+1):
            if mes <= i:
                mes = 13
                anio -= 1
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-i)
            demandas.append(prediccion_anterior.demandaReal)
        
        demanda_regresion = regresion_lineal(demandas, n)
        return demanda_regresion
    
    def metodo_estacional(self, prediccion, regresion):
        n = prediccion.cantPeriodos
        mes = prediccion.mesPrimerPeriodo
        anio = prediccion.anioPrimerPeriodo
        
        demandasActual = []
        demandasAnterior1 = []
        demandasAnterior2 = []
        for i in range(n):
            if mes <= i:
                mes = 13
                anio -= 1
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio-1, mesDemanda=mes-i)
            demandasActual.append(prediccion_anterior.demandaReal)
            
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio-2, mesDemanda=mes-i)
            demandasAnterior1.append(prediccion_anterior.demandaReal)
            
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio-3, mesDemanda=mes-i)
            demandasAnterior2.append(prediccion_anterior.demandaReal)
        
        demandaEstacional = estacionalidad(demandasActual, demandasAnterior1, demandasAnterior2, regresion)
        return demandaEstacional
    
    def metodo_cuadrado(self, prediccion, demanda):
        n = prediccion.cantPeriodos
        mes = prediccion.mesPrimerPeriodo
        anio = prediccion.anioPrimerPeriodo
        
        demandas = []
        for i in range(0,n):
            if mes <= i:
                mes = 13
                anio -= 1
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-i)
            demandas.append(prediccion_anterior.demandaReal)
        demandas_predecidas = [demanda]
        for i in range(1,n):
            if mes <= i:
                mes = 13
                anio -= 1
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-i)
            demandaP = prediccion_anterior.demandaPredecida
            if demandaP == 0:
                if mes <= i+1:
                    mes = 13+i
                    anio -= 1
                prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-(i+1))
                demandaP = prediccion_anterior.demandaReal
            demandas_predecidas.append(demandaP)
        
        error_cuadrado = error_cuadrado_medio(demandas, demandas_predecidas)
        return error_cuadrado
    
    def metodo_porcentual(self, prediccion, demanda):
        n = prediccion.cantPeriodos
        mes = prediccion.mesPrimerPeriodo
        anio = prediccion.anioPrimerPeriodo
        
        demandas = []
        for i in range(0,n):
            if mes <= i:
                mes = 13
                anio -= 1
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-i)
            demandas.append(prediccion_anterior.demandaReal)
        demandas_predecidas = [demanda]
        for i in range(1,n):
            if mes <= i:
                mes = 13
                anio -= 1
            prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-i)
            demandaP = prediccion_anterior.demandaPredecida
            if demandaP == 0:
                if mes <= i+1:
                    mes = 13+i
                    anio -= 1
                prediccion_anterior = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes-(i+1))
                demandaP = prediccion_anterior.demandaReal
            demandas_predecidas.append(demandaP)
        
        errorP = error_porcentual(demandas, demandas_predecidas)
        return errorP


class ResultadosDemanda(TemplateView):
    template_name = 'resultados_demanda.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resultados = self.request.session.get('resultados_prediccion', {})
        error_aceptable = resultados.get('error_aceptable')
        mes = resultados.get('mes_primer_periodo')
        anio = resultados.get('anio_primer_periodo')
        errores = {
            'Suavización Exponencial': resultados.get('error_exp'),
            'Promedio Móvil Ponderado': resultados.get('error_ponderado'),
            'Regresión Lineal': resultados.get('error_regresion'),
            'Estacional': resultados.get('error_estacional')
        }
        
        # Filtrar los errores que no son menores al error aceptable
        errores_validos = {metodo: error for metodo, error in errores.items() if error >= error_aceptable}
        
        # Encontrar el error más cercano al aceptable
        if errores_validos:
            error_cercano_metodo, error_cercano_valor = min(errores_validos.items(), key=lambda x: abs(x[1] - error_aceptable))
        else:
            error_cercano_metodo, error_cercano_valor = None, None
        
        context.update(resultados)
        context['error_cercano_metodo'] = error_cercano_metodo
        context['error_cercano_valor'] = error_cercano_valor
        
        if error_cercano_metodo == 'Suavización Exponencial':
            demanda_predecida = resultados.get("demanda_exponencial")
        elif error_cercano_metodo == "Promedio Móvil Ponderado":
            demanda_predecida = resultados.get("demanda_ponderado")
        elif error_cercano_metodo == "Regresión Lineal":
            demanda_predecida = resultados.get("demanda_regresion")
        elif error_cercano_metodo == "Estacional":
            demanda_predecida = resultados.get("demanda_estacional")
        else:
            demanda_predecida = None

        if demanda_predecida is not None:
            demanda_predecida = int(demanda_predecida)
            # Obtener la demanda para el periodo especificado
            demanda = get_object_or_404(Demanda, anioDemanda=anio, mesDemanda=mes)
            # Actualizar la demanda predicha con el valor de demanda aceptada
            demanda.demandaPredecida = demanda_predecida
            # Guardar la demanda actualizada
            demanda.save()
            
        return context


class AsignarProveedorView(UpdateView):
    model = Articulo
    form_class = AsignarProveedorForm
    template_name = 'asignar_proveedor.html'
    context_object_name = 'articulo'

    def form_valid(self, form):
        articulo = form.save(commit=False)
        proveedor = articulo.proveedor
        
        # verificar modelo de inventario
        modelo = articulo.modeloInventario.nombreMI
        codArt = articulo.codArticulo

        if modelo == "Lote Fijo":
            loteO = self.calcularLO(codArt, proveedor)
            puntoP = self.calcularPP(codArt, proveedor)
            stockS = self.calcularSSLote(proveedor)

            articulo.loteOptimo = loteO
            articulo.puntoPedido = puntoP
            articulo.stockSeguridad = stockS
        else:
            loteO = self.calcularIO(codArt, proveedor)
            puntoP = self.calcularPP(codArt, proveedor)
            stockS = self.calcularSSLote(proveedor)

            articulo.loteOptimo = loteO
            articulo.puntoPedido = puntoP
            articulo.stockSeguridad = stockS
        
        articulo.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lista_articulos')

# Lote Fijo
    def calcularLO(self, cod_articulo, proveedor):
        anio = datetime.now().year
        mes = datetime.now().month - 1

        cp = proveedor.costo_pedido
        demanda = get_object_or_404(Demanda, articulo=cod_articulo, anioDemanda=anio, mesDemanda=mes)
        d = demanda.demandaReal
        
        loteO = EOQ(d, cp)
        
        return loteO

    def calcularPP(self, cod_articulo, proveedor):
        anio = datetime.now().year
        mes = datetime.now().month - 1

        l = proveedor.diasDeDemora
        demanda = get_object_or_404(Demanda, articulo=cod_articulo, anioDemanda=anio, mesDemanda=mes)
        demandad = demanda.demandaReal / 30  # Esto supone que demanda es un valor total mensual
        
        puntoPedido = PP(demandad, l)
        
        return puntoPedido

    def calcularSSLote(self, proveedor):
        l = proveedor.diasDeDemora
        
        stockS = SSLF(l)
        
        return stockS
        
        
# Lote Fijo - MPR
    def calcularIO(self, cod_articulo, proveedor):
        anio = datetime.now().year
        mes = datetime.now().month - 1

        cp = proveedor.costo_pedido
        demanda = get_object_or_404(Demanda, articulo=cod_articulo, anioDemanda=anio, mesDemanda=mes)
        d = demanda.demandaReal
        ca = 10
        k = 100

        loteO = MPR(d,cp,ca,k)
        return loteO
        
    def calcularSSInventario(self, proveedor, cod_articulo):
        anio = datetime.now().year
        mes = datetime.now().month - 1

        l = proveedor.diasDeDemora
        cp = proveedor.costo_pedido
        demanda = get_object_or_404(Demanda, articulo=cod_articulo, anioDemanda=anio, mesDemanda=mes)
        dd = demanda.demandaReal / 30  # Esto supone que demanda es un valor total mensual
        ca = 10
        z = 1.64
        k = 100
        stockS = SSIF (dd,cp,ca,k,l,z)
        
        return stockS
        
def promedioExponencia(demandaPredecidaAnterior, demandaRealAnterior, cofSua):
    Xp = ceil(demandaPredecidaAnterior + cofSua * (demandaRealAnterior - demandaPredecidaAnterior))
    return Xp

def promedio_movil_ponderado(demanda, pesos):
    suma = 0
    for d, p in zip(demanda, pesos):
        suma += d * p
    demanda_predecida = ceil(suma)
    return demanda_predecida

def regresion_lineal(demandas, cantp):
    
    periodos = []
    
    for n in range(1,cantp+1):
        periodos.append(int(n))
    
    pd = statistics.mean(demandas) #Promedio Demanda
    px = statistics.mean(periodos)
    
    sumxy = 0
    for i in range(len(demandas)):
        sumxy += demandas[i] * periodos[i]
    
    sumx2 = 0
    for i in periodos:
        sumx2 += i**2
    
    b = (sumxy-cantp*pd*px)/(sumx2-cantp*px**2)
    
    a = pd-b*px
    
    demandapredecida=ceil(b*(cantp+1)+a)
    return demandapredecida

def estacionalidad(demandasActual, demandasPasado1, demandasPasado2, demandaRegresion):
    n = len(demandasActual)
    
    promedioMes = (demandasActual[0]+demandasPasado1[0]+demandasPasado2[0])/3
    print(promedioMes)
    
    promedios = []
    for i in range(n):
        promedios.append((demandasActual[i]+demandasPasado1[i]+demandasPasado2[i])/3) 
        
    indiceE = promedioMes/statistics.mean(promedios)
    
    demandaEstacionalidad = ceil(demandaRegresion*indiceE)
    return demandaEstacionalidad       
    
def error_cuadrado_medio(demandas_real, demandas_predecidas):
    sumatoria = 0
    for i in range(len(demandas_real)):
        sumatoria = (demandas_predecidas[i]-demandas_real[i])**2
    error_cm = sumatoria/len(demandas_real)
    return error_cm

def error_porcentual(demandas_real, demandas_predecidas):
    sumatoria = 0
    for i in range(len(demandas_real)):
        sumatoria = (demandas_predecidas[i]-demandas_real[i])*100/demandas_real[i]
    error_porcentual = sumatoria/len(demandas_real)
    return error_porcentual

def EOQ(d, cp):
    ca = 1
    q = sqrt(2*d*(cp/ca))
    return ceil(q)

def PP(dd,l):
    pp = dd * l
    return pp


#Sistema de Tamaño Fijo de Lote - MPR
def MPR(d,cp,ca,k):
    q = math.sqrt(2*d*(cp/ca)*(1/(1-(d/k))))
    return math.ceil(q)

## SS lote fijo
def SSLF (l):
    z = 1.64
    ss = z*sqrt(l)
    return ss
## SS intervalo fijo
def SSIF (dd,cp,ca,k,l,z):
    t =  math.sqrt((2/dd)*(cp/ca)*(1/(1-(dd/k))))
    ss = z*math.sqrt(t+l)
    return ss
