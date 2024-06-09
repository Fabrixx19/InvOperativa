from django import forms
from .models import *

# Aqui vamos a ingresar los valores que necesitamos para la prediccion

#Formulario para que el usuario ingrese mes y año
class DatosPrediccionFrom(forms.Form):
    mes = forms.ChoiceField(choices=[(str(i),i) for i in range(1,13)])
    anio = forms.ChoiceField(choices=[(str(i),i) for i in range(2000,2100)])


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        exclude = ['demanda'] # Agrega el campo 'demanda'
        widgets = {
            'fechaVenta': forms.DateInput(attrs={'type': 'date'}),
        }
    articulo = forms.ModelChoiceField(
        queryset=Articulo.objects.all(),
        widget=forms.Select,
        label="Artículo"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].queryset = Articulo.objects.all()
        self.fields['articulo'].label_from_instance = lambda obj: f"{obj.nombreArticulo}"


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombreArticulo', 'stockArticulo', 'estado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].empty_label = None
        self.fields['estado'].label_from_instance = lambda obj: obj.nombreEA


