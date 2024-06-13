from math import ceil

def promedioExponencia(demandaPredecidaAnterior, demandaRealAnterior, cofSua):
    Xp = ceil(demandaPredecidaAnterior + cofSua * (demandaRealAnterior - demandaPredecidaAnterior))
    return Xp

def promedio_movil_ponderado(demanda, pesos):
    suma = 0
    for d, p in zip(demanda, pesos):
        suma += d * p

    demanda_predecida = ceil(suma)
    return demanda_predecida

def regresion_lineal():
    Dr=[74,79,80,90,105,142,122]
    mes=[1,2,3,4,5,6,7]
    
    AxD = []
    for i in range(len(Dr)):
        AxD.append(Dr[i] * mes[i])
    print(AxD)
    
    #Funcion para calcular promedios
    def calcular_promedio(lista):
        if len(lista) == 0:
            return 0.0
        return sum(lista) / len(lista)
    
    def suma_de_cuadrados(lista):
        return sum(elemento ** 2 for elemento in lista)
    
    PD = calcular_promedio(Dr) #Promedio Demanda
    PM = calcular_promedio(mes) #Promedio mes
    sumaCuadradosAnio = suma_de_cuadrados(mes)
    print(f"El promedio general demanda real es: {PD:.2f}")
    print(f"El promedio general años es: {PM:.2f}")
    
    b = ((sum(AxD)- mes[-1]*PD*PM)/(sumaCuadradosAnio-mes[-1]*(PM**2)))
    print(f'b={b}')
    
    a = (PD-b*PM)
    print(f'a={a}')
    
    pronostico2008 = b*(mes[-1]+1)+a
    print(f'Pronostico2008={pronostico2008}')
    
def error_cuadrado_medio(demandas_real, demandas_predecidas):
    sumatoria = 0
    for i in range(len(demandas_real)):
        sumatoria = (demandas_predecidas[i]-demandas_real[i])**2
    error_cm = sumatoria/len(demandas_real)
    return error_cm

def error_porcentual():
    
    pass