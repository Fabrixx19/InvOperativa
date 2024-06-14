from math import ceil
import statistics

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
    print(indiceE)
    
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
    

