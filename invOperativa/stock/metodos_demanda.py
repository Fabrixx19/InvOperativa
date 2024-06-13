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
    #El calculo de error se hace con dos listas Dreal y Dpronosticada
    # lista error = abs[Dreal - Dpronosticada]
    mes = [1,2,3,4,5,6,7,8,9]
    Dr = [180,168,159,175,190,205,180,182]
    error = [5,7.5,15.8,1.8,16.6,30,2,3.8]
    def valor_absoluto_lista(error):
        return [abs(elemento) for elemento in error]

    absError = valor_absoluto_lista(error)
    print(f'El valor absoluto de la lista es: {absError}')

    def sumatoria(lista1, lista2):
        suma = 0
        for elemento1, elemento2 in zip(lista1, lista2):
            suma += (100 * elemento1 / elemento2)
        return suma

    sumatorai = sumatoria(absError, Dr)

    MAPE = sumatorai/(mes[-1]-1)