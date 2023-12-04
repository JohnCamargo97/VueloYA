from django import forms
from .models import Vuelo

class BusquedaForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = '__all__'