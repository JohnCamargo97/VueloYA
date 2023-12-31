from django import forms
from .models import userVueloYa
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


class UpdateUserVYaForm(forms.ModelForm):
    class Meta:
        model = userVueloYa
        widgets = {'picture': ClearableFileInput(attrs={'accept': 'application/png,application/jpg'})}
        fields = ('picture', 'genero', 'telefono', 'fechaNacimiento')
        