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
        queryset=Articulo.objects.filter(fechaBajaArticulo__isnull=True),
        widget=forms.Select,
        label="Artículo"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].queryset = Articulo.objects.filter(fechaBajaArticulo__isnull=True)
        self.fields['articulo'].label_from_instance = lambda obj: f"{obj.nombreArticulo}"


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombreArticulo', 'stockArticulo', 'estado', 'modeloInventario']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].empty_label = None
        self.fields['estado'].label_from_instance = lambda obj: obj.nombreEA
        self.fields['modeloInventario'].empty_label = None
        self.fields['modeloInventario'].label_from_instance = lambda obj: obj.nombreMI

class PrediccionDemandaForm(forms.ModelForm):
    class Meta:
        model = Prediccion_Demanda
        fields = ['cantPeriodos', 'coeficienteSuavizacion', 'articulo', 'errorAceptable', 'mesPrediccion', 'anioPrediccion', 'metodoError']
        
    pesos = forms.CharField(widget=forms.Textarea, help_text="Ingrese los pesos separados por comas.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['metodoError'].empty_label = None
        self.fields['metodoError'].label_from_instance = lambda obj: obj.nombreME
        self.fields['articulo'].empty_label = None
        self.fields['articulo'].label_from_instance = lambda obj: obj.nombreArticulo

class PrediccionExponencialForm(forms.ModelForm):
    class Meta:
        model = Prediccion_Demanda
        fields = ['coeficienteSuavizacion','mesPrediccion', 'anioPrediccion', 'articulo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].empty_label = None
        self.fields['articulo'].label_from_instance = lambda obj: obj.nombreArticulo

class PrediccionPonderadoForm(forms.ModelForm):
    class Meta:
        model = Prediccion_Demanda
        fields = ['cantPeriodos','mesPrediccion', 'anioPrediccion', 'articulo']
        
    pesos = forms.CharField(widget=forms.Textarea, help_text="Ingrese los pesos separados por comas.")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].empty_label = None
        self.fields['articulo'].label_from_instance = lambda obj: obj.nombreArticulo

class PrediccionRegresionForm(forms.ModelForm):
    class Meta:
        model = Prediccion_Demanda
        fields = ['cantPeriodos','mesPrediccion', 'anioPrediccion', 'articulo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].empty_label = None
        self.fields['articulo'].label_from_instance = lambda obj: obj.nombreArticulo

class PrediccionEstacionalForm(forms.ModelForm):
    class Meta:
        model = Prediccion_Demanda
        fields = ['cantPeriodos', 'mesPrediccion', 'anioPrediccion', 'articulo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].empty_label = None
        self.fields['articulo'].label_from_instance = lambda obj: obj.nombreArticulo

class AsignarProveedorForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['proveedor']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].empty_label = None
        self.fields['proveedor'].label_from_instance = lambda obj: obj.nombreProveedor


class OrdenDeCompraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        label="Proveedor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    articulo = forms.ModelChoiceField(
        queryset=Articulo.objects.filter(fechaBajaArticulo__isnull=True),
        label="Artículo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = OrdenDeCompra
        fields = ['cantidad', 'articulo', 'proveedor']
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].queryset = Articulo.objects.filter(fechaBajaArticulo__isnull=True)           
        self.fields['articulo'].label_from_instance = lambda obj: obj.nombreArticulo
        self.fields['proveedor'].empty_label = None
        self.fields['proveedor'].label_from_instance = lambda obj: obj.nombreProveedor
