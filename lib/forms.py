from django import forms
from .models import userVueloYa, aerolinea
from django.forms.widgets import ClearableFileInput
#from .models import Vuelo

class BusquedaForm(forms.Form):

    origen= forms.CharField(max_length=100, label='Origen', required=False)
    destino= forms.CharField(max_length=100, label='Destino', required=False)
    fechasalida= forms.DateField(label='Salida_d', required=False)
    fechavuelta= forms.DateField(label='vuelta_d', required=False)
    solo_ida= forms.BooleanField(label='solo_ida', required=False)
    ida_vuelta= forms.BooleanField(label='ida_vuelta', required=False)
    clase_economica= forms.BooleanField(label='clase_economica', required=False)
    clase_ejecutiva= forms.BooleanField(label='clase_ejecutiva', required=False)
    numero_pasajeros= forms.IntegerField(label='Pasajeros', required=False)
    
    #class Meta:
    #        model = Vuelo
    #        fields = '__all__'

class filtroForm(forms.Form):

    MONEDAS = [
        ("COP", "COP"),
        ("USD", "USD"),
        ("EUR", "EUR"),
    ]

    AEROLINEAS = aerolinea.objects.all().values_list('id', 'id')

    rango_precio = forms.IntegerField(max_value = 10000000, min_value=450000)
    moneda = forms.ChoiceField(choices=MONEDAS) 
    aerolinea = forms.MultipleChoiceField(choices=AEROLINEAS)

    


class UpdateUserVYaForm(forms.ModelForm):
    class Meta:
        model = userVueloYa
        widgets = {'picture': ClearableFileInput(attrs={'accept': 'application/png,application/jpg'})}
        fields = ('picture', 'genero', 'telefono', 'fechaNacimiento')

class voucherForm(forms.Form):
    email= forms.EmailField(required=True)
    emailConfirmacion= forms.EmailField(required=True)

class metodoPago(forms.Form):
    METODOS_PAGO_CHOICES = [
        ("tarjetacredito", "tarjetacredito"),
        ("tarjetadebito", "tarjetadebito"),
        ("pse", "pse"),
        ("criptomonedas", "criptomonedas"),
        ("efecty", "efecty"),
        ("sured", "sured"),
    ]

    metodopago = forms.ChoiceField(required=True, widget= forms.RadioSelect, choices=METODOS_PAGO_CHOICES)  
    
class datosTarjeta(forms.Form):
    numerodetarjeta= forms.IntegerField(required=False)
    titulartarjeta= forms.CharField(max_length=50, required=False)
    vencimiento= forms.CharField(max_length=5, required=False)
    codseguridad= forms.IntegerField(required=False)
    documentotitulartarjeta= forms.IntegerField(required= False)
    
class terminosyCondiciones(forms.Form):
    tyc= forms.BooleanField(required=True)
