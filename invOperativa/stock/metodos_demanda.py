import math
# la X de prediccion va a ser Xp
# la X de prediccion va a ser Xp
# La X de demanda real mes anterior Xra
Xpa = 142
Xra = 153
Alpha = 0.2
def promedioExponencia(Xpa, Xra, Alpha):
    Xp = math.ceil(Xpa + Alpha * (Xra - Xpa))
    return Xp

resultado = promedioExponencia(Xpa, Xra, Alpha)
print(f"El resultado de la predicción Xp es: {resultado}")