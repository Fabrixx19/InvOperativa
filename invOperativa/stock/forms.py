from django import forms
from .models import Prediccion_Demanda

# Aqui vamos a ingresar los valores que necesitamos para la prediccion

#Formulario para que el usuario ingrese mes y año
class DatosPrediccionFrom(forms.Form):
    mes = forms.ChoiceField(choices=[(str(i),i) for i in range(1,13)])
    anio = forms.ChoiceField(choices=[(str(i),i) for i in range(2000,2100)])
